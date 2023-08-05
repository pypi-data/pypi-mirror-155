import os
import csv
import xml
import re
import itertools
import subprocess
from functools import reduce
from operator import attrgetter
from collections import Counter, defaultdict
from abc import abstractmethod, ABCMeta

import numpy as np
import statsmodels.api as sm
from mass_spec_utils.data_import.mzmine import load_picked_boxes, \
    map_boxes_to_scans, PickedBox
from mass_spec_utils.data_import.mzml import MZMLFile

from vimms.Box import (
    Point, Interval, GenericBox,
    BoxLineSweeper
)
from vimms.Common import path_or_mzml


class EvaluationData():
    """
    A container class that wraps the Environment class, storing only relevant data for evaluation.
    This is useful for pickling/unpickling for evaluation as it will be much smaller.
    """
    def __init__(self, env):
        """
        Create an EvaluationData container
        Args:
            env: An instance of [vimms.Environment.Environment] object
        """
        # for compatibility with evaluate_simulated_env
        self.mass_spec = self.DummyMassSpec(env.mass_spec)
        self.controller = self.DummyController(env.controller)

        # for convenience
        self.chemicals = self.mass_spec.chemicals
        self.fragmentation_events = self.mass_spec.fragmentation_events
        self.scans = self.controller.scans

    class DummyMassSpec():
        def __init__(self, mass_spec):
            self.chemicals = mass_spec.chemicals
            self.fragmentation_events = mass_spec.fragmentation_events

    class DummyController():
        def __init__(self, controller):
            self.scans = controller.scans
            

def count_boxes(box_filepath):
    with open(box_filepath, "r") as f:
        return sum(ln.strip() != "" for ln in f) - 1

    
def pick_aligned_peaks(input_files,
                       output_dir,
                       output_name,
                       mzmine_template,
                       mzmine_exe,
                       force=False):
                       
    if(len(output_name.split(".")) > 1):
        output_name = "".join(output_name.split(".")[:-1])
    output_path = os.path.join(output_dir, f"{output_name}_aligned.csv")
    
    et = xml.etree.ElementTree.parse(mzmine_template)
    root = et.getroot()
    for child in root:
    
        if child.attrib["method"].endswith("RawDataImportModule"):
            input_found = False
            for e in child:
                if(e.attrib["name"].strip().lower() == "raw data file names"):
                    for f in e:
                        e.remove(f)
                    for i, fname in enumerate(input_files):
                        new = xml.etree.ElementTree.SubElement(e, "file")
                        new.text = fname
                        padding = " " * (0 if i == len(input_files) - 1 else 8)
                        new.tail = e.tail + padding
                    input_found = True
            assert input_found, "Couldn't find a place to put the input files in the template!"
                
        if child.attrib["method"].endswith("CSVExportModule"):
            for e in child:
                for f in e:
                    if f.tag == "current_file":
                        f.text = output_path
                            
    new_xml = os.path.join(output_dir, f"{output_name}_template.xml")
    et.write(new_xml)
    if(not os.path.exists(output_path) or force):
        subprocess.run([mzmine_exe, new_xml])
    
    try:
        num_boxes = count_boxes(output_path)
        print(f"Wrote {num_boxes} aligned boxes to file")
    except FileNotFoundError:
        raise FileNotFoundError("The box file doesn't seem to exist - did MZMine silently fail?")
        
    return output_path


class Evaluator(metaclass=ABCMeta):

    TIMES_FRAGMENTED = 0
    MAX_INTENSITY = 1
    MAX_FRAG_INTENSITY = 2

    def __init__(self, chems=[]):
        self.chems = chems
        self.chem_info = np.zeros((len(chems), 3, 0), dtype=float)

    @staticmethod
    def _new_window(rt, mz, isolation_width):
        width = isolation_width / 2
        return Interval(
            rt,
            rt,
            mz - width,
            mz + width
        )

    @abstractmethod
    def extra_info(self, report):
        pass

    def evaluation_report(self, min_intensity=0.0):
        chem_appears = np.any(self.chem_info[:, self.MAX_INTENSITY, :] >= min_intensity, axis=1)
    
        frag_counts = self.chem_info[chem_appears, self.TIMES_FRAGMENTED, :].T
        max_possible_intensities = self.chem_info[chem_appears, self.MAX_INTENSITY, :].T
        raw_intensities = self.chem_info[chem_appears, self.MAX_FRAG_INTENSITY, :].T
        
        coverage_intensities = raw_intensities * (raw_intensities >= min_intensity)
        coverage = np.array(coverage_intensities, dtype=np.bool)
        
        times_fragmented = np.sum(frag_counts, axis=0)
        times_fragmented_summary = Counter(times_fragmented.ravel())
        times_covered = np.sum(coverage, axis=0)
        times_covered_summary = Counter(times_covered.ravel())
        
        cumulative_coverage = list(itertools.accumulate(coverage, np.logical_or))
        cumulative_raw_intensities = list(itertools.accumulate(raw_intensities, np.fmax))
        cumulative_coverage_intensities = list(itertools.accumulate(coverage_intensities, np.fmax))
        
        num_chems = max_possible_intensities.shape[1]
        coverage_prop = np.sum(coverage, axis=1) / num_chems
        cumulative_coverage_prop = np.sum(cumulative_coverage, axis=1) / num_chems
        
        max_coverage_intensities = reduce(np.fmax, max_possible_intensities)
        which_non_zero = max_coverage_intensities > 0.0
        coverage_intensity_prop = [
            np.mean(c_i[which_non_zero] / max_coverage_intensities[which_non_zero]) 
            for c_i in coverage_intensities
        ]
        cumulative_raw_intensities_prop = [
            np.mean(c_i[which_non_zero] / max_coverage_intensities[which_non_zero])
            for c_i in cumulative_raw_intensities
        ]
        cumulative_coverage_intensities_prop = [
            np.mean(c_i[which_non_zero] / max_coverage_intensities[which_non_zero])
            for c_i in cumulative_coverage_intensities
        ]

        report = {
            "coverage" : coverage,
            "raw_intensity" : raw_intensities,
            "intensity" : coverage_intensities,
            "max_possible_intensity" : max_possible_intensities,
            
            "times_fragmented" : times_fragmented,
            "times_fragmented_summary" : times_fragmented_summary,
            "times_covered" : times_covered,
            "times_covered_summary" : times_covered_summary,
            
            "cumulative_coverage" : cumulative_coverage,
            "cumulative_raw_intensity" : cumulative_raw_intensities,
            "cumulative_intensity" : cumulative_coverage_intensities,
            
            "coverage_proportion" : list(coverage_prop),
            "intensity_proportion" : coverage_intensity_prop,
            "cumulative_raw_intensity_proportion" : cumulative_raw_intensities_prop,
            "cumulative_coverage_proportion" : list(cumulative_coverage_prop),
            "cumulative_intensity_proportion" : cumulative_coverage_intensities_prop
        }
            
        self.extra_info(report)
        return report
        

class SyntheticEvaluator(Evaluator):

    def __init__(self, chems=[]):
        super().__init__(chems=chems)
        self.envs = []

    @classmethod
    def from_envs(cls, envs):
        envs = list(envs)
    
        observed_chems = set(
            chem.get_original_parent() for env in envs for chem in env.mass_spec.chemicals
        )
        
        eva = cls(list(observed_chems))
        chem2idx = {ch : i for i, ch in enumerate(eva.chems)}
        
        for env in envs:
            eva.envs.append(env)
            new_info = np.zeros((len(eva.chems), 3, 1))
            
            for chem in env.mass_spec.chemicals:
                chem_idx = chem2idx[chem.get_original_parent()]
                new_info[chem_idx, cls.MAX_INTENSITY] = chem.max_intensity
                
            for event in env.mass_spec.fragmentation_events:
                if (event.ms_level > 1):
                    chem_idx = chem2idx[event.chem.get_original_parent()]
                    new_info[chem_idx, cls.TIMES_FRAGMENTED] += 1
                    new_info[chem_idx, cls.MAX_FRAG_INTENSITY] = max(
                        event.parents_intensity[0],
                        new_info[chem_idx, cls.MAX_FRAG_INTENSITY]
                    )
                
            eva.chem_info = np.concatenate((eva.chem_info, new_info), axis=2)
            
        return eva
    
    def extra_info(self, report):
        num_frags = [
            sum(event.ms_level > 1 for event in env.mass_spec.fragmentation_events)
            for env in self.envs
        ]
        report["num_frags"] = num_frags


#TODO: these are only here for backwards compatibility - can delete?
def evaluate_multiple_simulated_env(envs, min_intensity=0.0, group_list=None):
    """Evaluates_multiple simulated injections against a base set of chemicals that
    were used to derive the datasets"""
    eva = SyntheticEvaluator.from_envs(envs)
    return eva.evaluation_report(min_intensity=min_intensity)

    
def evaluate_simulated_env(env, min_intensity=0.0, base_chemicals=None):
    """Evaluates a single simulated injection against the chemicals present in that injection"""
    return evaluate_multiple_simulated_env([env], min_intensity=min_intensity)

    
class RealEvaluator(Evaluator):
    def __init__(self, chems=[]):
        super().__init__(chems=chems)
        self.fullscan_names = []
        self.mzmls = []

    @classmethod
    def from_aligned(cls, aligned_file):
        include = [
                "status",
                "RT start",
                "RT end",
                "m/z min",
                "m/z max"
            ]
    
        chems = []
        with open(aligned_file, "r") as f:
            headers = f.readline().split(",")
            pattern = re.compile(r"(.*).mzML filtered Peak ([a-zA-Z/]+( [a-zA-Z/]+)*)")
            
            indices = defaultdict(dict)
            for i, h in enumerate(headers):
                m = pattern.match(h)
                if(not m is None):
                    indices[m.group(1)][m.group(2)] = i
            
            for ln in f:
                row = []
                split = ln.split(",")
                for fname, inner in indices.items():
                    if(split[inner["status"]] == "DETECTED"):
                        row.append(
                            GenericBox(
                                float(split[inner["RT start"]]) * 60,
                                float(split[inner["RT end"]]) * 60,
                                float(split[inner["m/z min"]]),
                                float(split[inner["m/z max"]])
                            )
                        )
                    else:
                        row.append(None)
                chems.append(row)
                
        eva = cls(chems)
        eva.fullscan_names = list(indices.keys())
        return eva
        
    def add_info(self, fullscan_name, mzmls, isolation_width=None):
        geom = BoxLineSweeper()
        if("." in fullscan_name): fullscan_name = ".".join(fullscan_name.split(".")[:-1])
        fs_idx = self.fullscan_names.index(os.path.basename(fullscan_name))
        chems = [row[fs_idx] for row in self.chems]
        box2idx = {box : i for i, box in enumerate(chems)}
        geom.register_boxes(ch for ch in chems if not ch is None)
        
        for mzml in mzmls:
            mzml = path_or_mzml(mzml)
            self.mzmls.append(mzml)
            new_info = np.zeros((len(chems), 3, 1))
            
            for s in sorted(mzml.scans, key=attrgetter("rt_in_seconds")):
                geom.set_active_boxes(s.rt_in_seconds)
                if(s.ms_level == 1):
                    current_intensities = [[] for _ in self.chems]
                    
                    for mz, intensity in s.peaks:
                        related_boxes = geom.point_in_which_boxes(
                            Point(s.rt_in_seconds, mz)
                        )
                        
                        for b in related_boxes:
                            idx = box2idx[b]
                            current_intensities[idx].append((mz, intensity))
                            new_info[idx, self.MAX_INTENSITY] = max(
                                intensity,
                                new_info[idx, self.MAX_INTENSITY]
                            )
                else:
                    mz = s.precursor_mz
                    if(isolation_width is None):
                        related_boxes = geom.point_in_which_boxes(
                            Point(s.rt_in_seconds, mz)
                        )

                        for b in related_boxes:
                            idx = box2idx[b]
                            candidates = [
                                cint for cmz, cint in current_intensities[idx]
                                if cmz >= mz - 1E-10 and cmz <= mz + 1E-10
                            ]
                            new_info[idx, self.TIMES_FRAGMENTED] += 1
                            new_info[idx, self.MAX_FRAG_INTENSITY] = max(
                                max(candidates + [0.0]),
                                new_info[idx, self.MAX_FRAG_INTENSITY]
                            )
                    else:
                        related_boxes = geom.interval_covers_which_boxes(
                            self._new_window(s.rt_in_seconds, mz, isolation_width)
                        )

                        for b in related_boxes:
                            idx = box2idx[b]
                            new_info[idx, self.TIMES_FRAGMENTED] += 1
                            new_info[idx, self.MAX_FRAG_INTENSITY] = max(
                                max([it for _, it in current_intensities[idx]] + [0.0]),
                                new_info[idx, self.MAX_FRAG_INTENSITY]
                            )
            self.chem_info = np.concatenate((self.chem_info, new_info), axis=2)

    def extra_info(self, report):
        num_frags = []
        for mzml in self.mzmls:
            mzml = path_or_mzml(mzml)
            num_frags.append(
                sum(s.ms_level == 2 for s in mzml.scans)
            )
        report["num_frags"] = num_frags
        
    def clear_info(self):
        self.chem_info[:] = 0
        self.mzmls = []
        
        
def evaluate_real(aligned_file,
                  mzml_map,
                  isolation_width=None, 
                  min_intensity=0.0):
    """
    Produce combined evaluation report on real data stored in .mzmls.
    Args:
        aligned_file: Filepath of an MZMine peak-picking output file.
        mzml_map: Dictionary mapping filepaths of fullscans which have been
                  peak-picked, to lists of .mzmls which should be evaluated 
                  using their parent fullscan's picked peaks. 
                  .mzmls can be specified as either a filepath or an MZMLFile 
                  object.
        isolation_width: isolation width to use for evaluating whether a
                         fragmentation event is a hit.
                         None if the fragmentation event has to lie exactly
                         within the box.
                         Otherwise, checks if an interval of the specified
                         length entirely covers the box on the m/z dimension.
        min_intensity: Fragmentation events with precursor below this threshold
                       do not count as hits.

    Returns: A dictionary mapping names to evaluation statistics.
    """

    eva = RealEvaluator.from_aligned(aligned_file)
    for fullscan_path, mzmls in mzml_map.items():
        fullscan_name = os.path.basename(fullscan_path)
        eva.add_info(fullscan_name, mzmls, isolation_width=isolation_width)
    return eva.evaluation_report(min_intensity=min_intensity)


def calculate_chemical_p_values(datasets, group_list, base_chemicals):
    # only accepts case control currently
    p_values = []
    # create y here
    categories = np.unique(np.array(group_list))
    if len(categories) < 2:
        pass
    elif len(categories):
        x = np.array([1 for i in group_list])
        if 'control' in categories:
            control_type = 'control'
        else:
            control_type = categories[0]
        x[np.where(np.array(group_list) == control_type)] = 0
        x = sm.add_constant(x)
    else:
        pass
    # create each x and calculate p-value
    ds_parents = [[chem.base_chemical for chem in ds] for ds in datasets]
    for chem in base_chemicals:
        y = []
        for i, ds in enumerate(ds_parents):
            if chem in base_chemicals:
                new_chem = \
                    np.array(datasets[i])[np.where(np.array(ds) == chem)[0]][0]
                intensity = np.log(new_chem.max_intensity + 1)
            else:
                intensity = 0.0
            y.append(intensity)
        model = sm.OLS(y, x)
        p_values.append(model.fit(disp=0).pvalues[1])
    return p_values


def evaluate_mzml(mzml_file, picked_peaks_file, half_isolation_window):
    boxes = load_picked_boxes(picked_peaks_file)
    mz_file = MZMLFile(mzml_file)
    scans2boxes, boxes2scans = map_boxes_to_scans(mz_file, boxes,
                                                  half_isolation_window=half_isolation_window)
    coverage = len(boxes2scans)
    return coverage


def load_xcms_boxes(box_file):
    boxes = load_picked_boxes(box_file)
    for box in boxes:
        box.rt_in_seconds /= 60.
        box.rt_range_in_seconds = [r / 60. for r in box.rt_range_in_seconds]
        box.rt /= 60.
        box.rt_range = [r / 60. for r in box.rt_range]
    return boxes


def load_peakonly_boxes(box_file):
    boxes = []
    with open(box_file, 'r') as f:
        reader = csv.reader(f)
        # heads = next(reader)
        for line in reader:
            peak_id = int(line[0])
            peak_mz = float(line[1])
            rt_min = 60.0 * float(line[2])
            rt_max = 60.0 * float(line[3])
            height = float(line[4])
            new_box = PickedBox(peak_id, peak_mz, rt_max + rt_min / 2, peak_mz,
                                peak_mz, rt_min, rt_max, height=height)
            boxes.append(new_box)
    boxes.sort(key=lambda x: x.rt)
    return boxes


def evaluate_peak_roi_aligner(roi_aligner, source_file,
                              evaluation_mzml_file=None,
                              half_isolation_width=0):
    coverage, coverage_intensities, max_possible_intensities, included_peaksets = [], [], [], []

    for i, peakset in enumerate(roi_aligner.peaksets):
        source_files = {peak.source_file: i for i, peak in
                        enumerate(peakset.peaks)}
        if source_file in source_files:
            which_peak = source_files[source_file]
            max_possible_intensities.append(
                peakset.peaks[which_peak].intensity)
            if evaluation_mzml_file is not None:
                boxes = [box for box, name in zip(roi_aligner.list_of_boxes,
                                                  roi_aligner.sample_names) if
                         name == source_file]
                scans2boxes, boxes2scans = map_boxes_to_scans(
                    evaluation_mzml_file, boxes,
                    half_isolation_window=half_isolation_width)
                precursor_intensities, scores = get_precursor_intensities(
                    boxes2scans, boxes, 'max')
                temp_max_possible_intensities = max_possible_intensities
                max_possible_intensities = [max(*obj) for obj in
                                            zip(precursor_intensities,
                                                temp_max_possible_intensities)]
                # TODO: actually check that this works
            fragint = roi_aligner.peaksets2fragintensities[peakset][which_peak]
            coverage_intensities.append(fragint)
            included_peaksets.append(i)
        else:
            coverage_intensities.append(0.0)  # fragmentation intensity
            max_possible_intensities.append(
                0.0)  # max possible intensity (so highest observed ms1 intensity)
    included_peaksets = np.array(included_peaksets)
    max_possible_intensities = np.array(max_possible_intensities)
    coverage_intensities = np.array(coverage_intensities)
    coverage = coverage_intensities > 1
    coverage_prop = sum(coverage[included_peaksets]) / len(
        coverage[included_peaksets])
    coverage_intensity_prop = np.mean(
        coverage_intensities[included_peaksets] / max_possible_intensities[
            included_peaksets])

    return {
        'coverage': coverage,
        'intensity': coverage_intensities,
        'coverage_proportion': coverage_prop,
        'intensity_proportion': coverage_intensity_prop,
        'max_possible_intensities': max_possible_intensities,
        'included_peaksets': included_peaksets
    }


def evaluate_multi_peak_roi_aligner(frequentist_roi_aligner, source_files,
                                    casecontrol=False):
    results = [evaluate_peak_roi_aligner(frequentist_roi_aligner, file) for file
               in source_files]
    coverage = [r['coverage'] for r in results]
    coverage_intensities = [r['intensity'] for r in results]
    max_possible_intensities_experiment = [r['max_possible_intensities'] for r
                                           in results]
    max_possible_intensities = reduce(np.fmax,
                                      max_possible_intensities_experiment)
    cumulative_coverage_intensities = list(
        itertools.accumulate(coverage_intensities, np.fmax))
    cumulative_coverage = list(itertools.accumulate(coverage, np.logical_or))
    cumulative_coverage_prop = [np.sum(cov) / len(max_possible_intensities) for
                                cov in cumulative_coverage]
    cumulative_coverage_intensities_prop = [
        np.mean(c_i / max_possible_intensities) for c_i in
        cumulative_coverage_intensities]
    coverage_times_fragmented = [sum(i) for i in zip(*coverage)]
    if casecontrol:
        pvalues = frequentist_roi_aligner.get_p_values(casecontrol)
    else:
        pvalues = [None for ps in frequentist_roi_aligner.peaksets]

    return {
        'coverage': coverage,
        'intensity': coverage_intensities,
        'cumulative_intensity': cumulative_coverage_intensities,
        'cumulative_coverage': cumulative_coverage,
        'cumulative_coverage_proportion': cumulative_coverage_prop,
        'cumulative_intensity_proportion': cumulative_coverage_intensities_prop,
        'coverage_times_fragmented': coverage_times_fragmented,
        'max_possible_intensity': max_possible_intensities,
        'pvalues': pvalues
    }


def get_precursor_intensities(boxes2scans, boxes, method):
    assert method in ['max', 'first']
    precursor_intensities = []
    scores = []
    for i, box in enumerate(boxes):
        if box in boxes2scans:
            scans = boxes2scans[box]
            scans = sorted(scans, key=lambda s: s.rt_in_seconds)

            # A box can be linked to multiple ms2 scans.
            # Here we get all the ms2 scans that overlap a box.
            # For each ms2 scan, we then find its precursor intensity using the last ms1 scan
            box_intensities = []
            for ms2_scan in scans:
                precursor = ms2_scan.previous_ms1.get_precursor(
                    ms2_scan.precursor_mz)
                if precursor is not None:
                    box_intensities.append(
                        precursor[1])  # precursor is (mz, intensity)

            if method == 'max':
                # for each box, get the max precursor intensity
                if len(box_intensities) > 0:
                    intensity = max(box_intensities)
                    score = intensity / box.height
                    precursor_intensities.append(intensity)
                    scores.append(score)
                else:
                    precursor_intensities.append(0.0)
                    scores.append(0.0)

            elif method == 'first':
                # for each box, get the first precursor intensity (smallest RT)
                intensity = box_intensities[0]
                score = intensity / box.height
                precursor_intensities.append(intensity)
                scores.append(score)
        else:
            precursor_intensities.append(0.0)
            scores.append(0.0)

    precursor_intensities = np.array(precursor_intensities)
    scores = np.array(scores)
    return precursor_intensities, scores