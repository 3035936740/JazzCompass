import re, random

class ChordConverter:
    def __init__(self):
        # Define basic note names and their corresponding indices
        self.note_to_idx = {
            'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3, 'E': 4,
            'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8, 'Ab': 8, 'A': 9,
            'A#': 10, 'Bb': 10, 'B': 11, 'Cb': 11, 'E#': 5, 'Fb': 4, 'B#': 0
        }
        # Map indices back to note names (defaults to sharps or standard names)
        self.idx_to_note = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

        # These numbers represent the semitone distance from the root (0)
        self.chord_formulas = {
            # --- Basic/Abbreviations ---
            "5": [0, 7],
            "major": [0, 4, 7],
            "maj": [0, 4, 7],
            "M": [0, 4, 7],
            "": [0, 4, 7],
            "minor": [0, 3, 7],
            "min": [0, 3, 7],
            "m": [0, 3, 7],
            "aug": [0, 4, 8],
            "dim": [0, 3, 6],
            "sus2": [0, 2, 7],
            "sus4": [0, 5, 7],
            "p4": [0, 5, 10], # pure 4th
            "t4": [0, 5, 11], # tritone
            "majB5": [0, 4, 6],
            "Mb5": [0, 4, 6],

            # --- 6th Chords ---
            "6": [0, 4, 7, 9],
            "m6": [0, 3, 7, 9],
            "6add9": [0, 4, 7, 9, 14],
            "m6add9": [0, 3, 7, 9, 14],
            "6sus4": [0, 5, 7, 9],

            # --- 7th Chords ---
            "7": [0, 4, 7, 10],
            "m7": [0, 3, 7, 10],
            "M7": [0, 4, 7, 11],
            "maj7": [0, 4, 7, 11],
            "m-maj7": [0, 3, 7, 11],
            "m-M7": [0, 3, 7, 11],
            "7sus4": [0, 5, 7, 10],
            "dim7": [0, 3, 6, 9],
            "m7b5": [0, 3, 6, 10],
            "m7b9": [0, 3, 7, 10, 13],
            "7b5": [0, 4, 6, 10],
            "7#5": [0, 4, 8, 10],
            "7b9": [0, 4, 7, 10, 13],
            "7#9": [0, 4, 7, 10, 15],
            "7#11": [0, 4, 7, 10, 18],
            "7add11": [0, 4, 7, 10, 17],
            "7add13": [0, 4, 7, 10, 21],
            "7#5b9": [0, 4, 8, 10, 13],
            "7#5#9": [0, 4, 8, 10, 15],
            "7b5b9": [0, 4, 6, 10, 13],

            # --- 9th Chords ---
            "9": [0, 4, 7, 10, 14],
            "m9": [0, 3, 7, 10, 14],
            "maj9": [0, 4, 7, 11, 14],
            "M9": [0, 4, 7, 11, 14],
            "m9-maj7": [0, 3, 7, 11, 14],
            "m9-M7": [0, 3, 7, 11, 14],
            "9sus4": [0, 5, 7, 10, 14],
            "9b5": [0, 4, 6, 10, 14],
            "m9b5": [0, 3, 6, 10, 14],
            "9#5": [0, 4, 8, 10, 14],
            "9#11": [0, 4, 7, 10, 14, 18],
            "9b13": [0, 4, 7, 10, 14, 20],
            "add9": [0, 4, 7, 14],
            "madd9": [0, 3, 7, 14],

            # --- 11th & 13th ---
            "11": [0, 4, 7, 10, 14, 17],
            "m11": [0, 3, 7, 10, 14, 17],
            "maj11": [0, 4, 7, 11, 14, 17],
            "M11": [0, 4, 7, 11, 14, 17],
            "11b9": [0, 4, 7, 10, 13, 17],
            "13": [0, 4, 7, 10, 14, 17, 21],
            "m13": [0, 3, 7, 10, 14, 17, 21],
            "maj13": [0, 4, 7, 11, 14, 17, 21],
            "M13": [0, 4, 7, 11, 14, 17, 21],
            "13b9": [0, 4, 7, 10, 13, 17, 21],
            "13#9": [0, 4, 7, 10, 15, 17, 21],
            "13b5b9": [0, 4, 6, 10, 13, 17, 21],

            # --- Special Combos ---
            "maj7#5": [0, 4, 8, 11],
            "maj7#11": [0, 4, 7, 11, 18],
            "maj7b5": [0, 4, 6, 11],
            "maj7add13": [0, 4, 7, 11, 21],
            "maj9#5": [0, 4, 8, 11, 14],
            "maj9#11": [0, 4, 7, 11, 14, 18],
            "maj9sus4": [0, 5, 7, 11, 14],
            "M7#5": [0, 4, 8, 11],
            "M7#11": [0, 4, 7, 11, 18],
            "M7b5": [0, 4, 6, 11],
            "M7add13": [0, 4, 7, 11, 21],
            "M9#5": [0, 4, 8, 11, 14],
            "M9#11": [0, 4, 7, 11, 14, 18],
            "M9sus4": [0, 5, 7, 11, 14],
            "m7add11": [0, 3, 7, 10, 17],
            "m7add13": [0, 3, 7, 10, 21],
            "m-maj7add11": [0, 3, 7, 11, 17],
            "m-maj7add13": [0, 3, 7, 11, 21],
            "m-maj11": [0, 3, 7, 11, 14, 17],
            "m-maj13": [0, 3, 7, 11, 14, 17, 21],
            "m-M7add11": [0, 3, 7, 11, 17],
            "m-M7add13": [0, 3, 7, 11, 21],
            "m-M11": [0, 3, 7, 11, 14, 17],
            "m-M13": [0, 3, 7, 11, 14, 17, 21]
        }
        
        self.reverse_formulas = {tuple(sorted(v)): k for k, v in self.chord_formulas.items()}

    def parse(self, input_str: str) -> set:
        """Convenience method to directly get note names from input string"""
        result = self.parse_and_get_notes(input_str)
        if isinstance(result, str):
            return result
        return result["notes"]

    def parse_slash_chord(self, input_str: str):
        """Parse slash chord logic: chord/bass note"""
        if "/" not in input_str:
            return None
            
        chord_part, bass_part = input_str.split("/", 1)
        # Get the notes of the upper chord
        upper_chord_res = self.parse_and_get_notes(chord_part)
        
        if isinstance(upper_chord_res, str):
            return upper_chord_res
            
        # Validate that the bass note is valid
        if bass_part not in self.note_to_idx:
            raise ValueError(f"Invalid bass note: {bass_part}")
    
        # Extract upper structure notes and remove duplicates (prevent duplication if bass note is already in the chord)
        upper_notes = upper_chord_res["notes"]
            
        # Use list comprehension or set to filter out notes identical to bass_part, ensuring the bass note is exclusively positioned first
        # Note: Standardize comparisons here to prevent mismatches between enharmonic equivalents (e.g., C# vs Db)
        std_bass = self.idx_to_note[self.note_to_idx[bass_part]]
        other_notes = [n for n in upper_notes if self.idx_to_note[self.note_to_idx[n]] != std_bass]
            
        # Place the bass note at index 0, followed by the remaining notes
        final_notes = [bass_part] + other_notes

        # Calculate offsets (maintaining the corresponding order)
        final_offsets = [self.note_to_idx[n] for n in final_notes]
        
        return {
            "chord": input_str,
            "notes": final_notes,
            "offsets": final_offsets,
            "is_slash": True
        }

    def parse_and_get_notes(self, input_str: str):
        """
        Core method: Parse strings like 'G#Major' or 'Gb7'
        """
        # 1. Preprocessing: If it's a slash chord, use special logic
        if "/" in input_str:
            return self.parse_slash_chord(input_str)
            
        # 2. Original standard chord parsing logic
        match = re.match(r"^([A-G][#b]?)(.*)$", input_str)
        if not match:
            raise ValueError(f"Unable to parse: {input_str}")
        
        root = match.group(1)
        chord_type = match.group(2)
        
        if not chord_type:
            chord_type = "maj"
            
        return self.get_chord_notes(root, chord_type)

    def get_chord_notes(self, root: str, chord_type="maj"):
        """
        Input root and chord type, output corresponding note list and offset indices
        """
        if root not in self.note_to_idx:
            return "Invalid root"
        
        root_idx = self.note_to_idx[root]
        
        # If chord type is not defined, default to major triad
        offsets = self.chord_formulas.get(chord_type, [0, 4, 7])
        
        # Calculate absolute indices (Modulo 12 ensures octave cycling)
        abs_indices = [(root_idx + o) % 12 for o in offsets]
        # Get note names
        note_names = [self.idx_to_note[i] for i in abs_indices]
        
        return {
            "chord": f"{root}{chord_type}",
            "notes": note_names,
            "offsets": abs_indices,
            "is_slash": False
        }
    
    def _ensure_notes_and_root(self, chord_input):
        """Unify input processing: Return (list of notes, root note)"""
        if isinstance(chord_input, str):
            data = self.parse_and_get_notes(chord_input)
            return data["notes"]
        elif isinstance(chord_input, (list, set, tuple)):
            notes = list(chord_input)
            return notes
        return None

class EnhancedChordConverter(ChordConverter):
    def __init__(self):
        super().__init__()
        self.interval_map = {
            '1': 0, 'b2': 1, '2b': 1, '2': 2, '#2': 3, '2#': 3, 'b3': 3, '3b': 3, '3': 4,
            '4': 5, '#4': 6, '4#': 6, 'b5': 6, '5b': 6, '5': 7, '#5': 8, '5#': 8, 'b6': 8, '6b': 8,
            '6': 9, 'bb7': 9, '7bb': 9, '#6': 10, '6#': 10, 'b7': 10, '7b': 10, '7': 11, 'maj7': 11, '7maj': 11,
            '9': 14, 'b9': 13, '9b': 13, '#9': 15, '9#': 15, '11': 17, '#11': 18, '11#': 18, '13': 21, 'b13': 20, '13b': 20
        }
        
        self.reverse_formulas = {tuple(sorted(v)): k for k, v in self.chord_formulas.items()}

    def parse_and_get_notes(self, input_str: str):
        if "/" in input_str:
            return self.parse_slash_chord(input_str)

        # 1. Extract the root note (A-G + #/b)
        root_match = re.match(r"^([A-G][#b]?)(.*)$", input_str)
        if not root_match:
            raise ValueError(f"Invalid root in: {input_str}")
        
        root = root_match.group(1)
        remaining = input_str[len(root):]

        # 2. Extract modifiers (add/omit)
        # Use regex to extract add/omit and the content following them
        modifiers = re.findall(r"(add|omit)\s*([#b]?\d+)", remaining)
        
        # 3. Determine the main chord type (the basic type is the part after the root and before any modifiers)
        # For example, "Cm add9" -> the main part is "m"
        main_type_part = re.split(r"add|omit", remaining)[0].strip()
        if not main_type_part:
            main_type_part = "maj"
        
        # Get the initial offset
        offsets = list(self.chord_formulas.get(main_type_part, [0, 4, 7]))

        # 4. Process modifiers
        for action, interval in modifiers:
            # Standardize the interval format, for example 7b -> b7
            norm_interval = self._normalize_interval(interval)
            semitone = self.interval_map.get(norm_interval)
            
            if semitone is None:
                continue

            if action == "add":
                if semitone not in [o % 12 for o in offsets]:
                    offsets.append(semitone)
            elif action == "omit":
                # Remove all duplicate notes within the octave
                offsets = [o for o in offsets if o % 12 != semitone % 12]

        return self._build_result(root, main_type_part, offsets, input_str)

    def _normalize_interval(self, interval: str):
        """Convert 7b to b7, leave #11 unchanged"""
        if len(interval) > 1 and interval[-1] in ['#', 'b']:
            return interval[-1] + interval[:-1]
        return interval

    def _build_result(self, root, chord_type, offsets, original_str):
        root_idx = self.note_to_idx[root]
        
        unique_abs_indices = set((root_idx + o) % 12 for o in offsets)
        
        if root_idx in unique_abs_indices:
            unique_abs_indices.remove(root_idx)
        
        sorted_others = sorted(list(unique_abs_indices))
        
        final_abs_indices = [root_idx] + sorted_others
        
        note_names = [self.idx_to_note[i] for i in final_abs_indices]
        
        return {
            "chord": original_str,
            "notes": note_names,
            "offsets": final_abs_indices,
            "is_slash": False,
            "root": root,
            "quality": chord_type
        }

    def _ensure_notes_and_root(self, chord_input, is_detailed = False):
        """Unify input processing: Return (list of notes, root note)"""
        result = None
        if isinstance(chord_input, str):
            data = self.parse_and_get_notes(chord_input)
            if is_detailed:
                result = data
            else:
                result = data["notes"]
        elif isinstance(chord_input, (list, set, tuple)):
            if is_detailed:
                root_note = chord_input[0]
                notes_index = [self.note_to_idx.get(n) for n in chord_input]
                rt_index_v = notes_index[0]
                
                notes_index_new = []
                
                last_value = None
                for idx in notes_index:
                    if last_value is not None and idx < last_value:
                        idx += 12  # Adjust for octave wraparound
                    notes_index_new.append(idx - rt_index_v)
                    
                    last_value = idx
                key = None
                target_tuple = tuple(sorted(notes_index_new))
                if target_tuple in self.reverse_formulas:
                    key = self.reverse_formulas[target_tuple]
                else:
                    raise ValueError(f"Unable to identify chord for notes: {chord_input} with offsets: {notes_index_new}")
                    
                chord = f"{root_note}{key}"
                result = {
                    "chord": chord,
                    "notes": list(chord_input),
                    "offsets": notes_index_new,
                    "is_slash": False,
                    "root": root_note,
                    "quality": key
                }
            else:
                result = list(chord_input)
            
        return result

    def identify_chord(self, indices : list | tuple | set):
        """
        Reverse engineer chord name by note index
        """
        root_name = self.idx_to_note[indices[0]]
        indices = sorted([i % 12 for i in set(indices)])
        n_notes = len(indices)
        
        result = {
            "chord": None,
            "root": root_name,
            "quality": None
        }
        
        # Try the possibility of each note as the root
        for i in range(n_notes):
            root = indices[i]
            offsets = sorted([(idx - root) % 12 for idx in indices])
            offsets_tuple = tuple(offsets)
            
            # Precise matching formula library
            if offsets_tuple in self.reverse_formulas:
                quality = self.reverse_formulas[offsets_tuple]
                # Handle empty strings (major triads are usually an empty string or "maj")
                quality_display = quality if quality else ""
                
                result["chord"] = f"{root_name}{quality_display}"
                result["quality"] = quality_display
                
                return result

        # If no match is found, use Add/Omit logic (based on the first note)
        root = indices[0]
        # Simplified approach here: List all interval names relative to the root note
        intervals = [(idx - root) % 12 for idx in indices[1:]]
        
        result["chord"] = f"{root_name}(add {','.join(map(str, intervals))})"
        result["quality"] = f"add {','.join(map(str, intervals))}"
        
        return result

class BluesToolkit:
    def __init__(self):        
        self.scale_metadata = {
            "Minor Blues": {"intervals": [0, 3, 5, 6, 7, 10], "blue_notes": [3, 6, 10]},
            "Major Blues": {"intervals": [0, 2, 3, 4, 7, 9], "blue_notes": [3]},
            "Mixolydian Blues": {"intervals": [0, 2, 3, 4, 5, 7, 9, 10], "blue_notes": [3, 10]},
            "Lydian Dominant": {"intervals": [0, 2, 4, 6, 7, 9, 10], "blue_notes": [6]},
            "Major Pentatonic": {"intervals": [0, 2, 4, 7, 9], "blue_notes": []},
            "Minor Pentatonic": {"intervals": [0, 3, 5, 7, 10], "blue_notes": []},
        }
    
    def _get_scale_details(self, root, scale_name, chord_offsets):
        """Enhanced version: Calculate the notes and label their relationship to the chord."""
        converter = EnhancedChordConverter()
        meta = self.scale_metadata.get(scale_name, {"intervals": []})
        root_idx = converter.note_to_idx[root]
        
        detailed_notes = []
        for i in meta["intervals"]:
            note_name = converter.idx_to_note[(root_idx + i) % 12]
            tags = []
            if i in meta.get("blue_notes", []): tags.append("BLUE")
            if i in chord_offsets: tags.append("CHORD_TONE")
            else: tags.append("TENSION")
            
            detailed_notes.append({
                "note": note_name,
                "role": "/".join(tags)
            })
        return detailed_notes

    def _calculate_scale_notes(self, root, scale_name):
        """Calculate the specific notes based on the root and scale name"""
        converter = EnhancedChordConverter()
        if scale_name not in self.scale_metadata:
            return []
        
        root_idx = converter.note_to_idx[root]
        intervals = self.scale_metadata[scale_name]["intervals"]
        
        # Convert to specific note names
        return [converter.idx_to_note[(root_idx + i) % 12] for i in intervals]

    def suggest_for_chord(self, chord_input):
        """
        Recommend a tonal scale, including the specific notes.
        Return format: [(scale name, reason, list of notes)]
        """
        converter = EnhancedChordConverter()
        notes = converter._ensure_notes_and_root(chord_input)
        if not notes: return []
            
        root = notes[0]
        root_idx = converter.note_to_idx[root]
        chord_offsets = set([(converter.note_to_idx[n] - root_idx) % 12 for n in notes])
        
        # Relative minor root
        rel_minor_root = converter.idx_to_note[(root_idx - 3) % 12]
        
        raw_suggestions = []
        
        # Logical judgment
        has_major_3rd = 4 in chord_offsets
        has_b7 = 10 in chord_offsets
        has_minor_3rd = 3 in chord_offsets

        if has_major_3rd and has_b7:
            raw_suggestions.append((root, "Mixolydian Blues", "Parallel: Classic jazz-blues sound"))
            raw_suggestions.append((root, "Minor Blues", "Parallel: 'Blue' tension over major chord"))
            raw_suggestions.append((rel_minor_root, "Minor Pentatonic", "Relative: Sweet country-blues color"))
        elif has_minor_3rd:
            raw_suggestions.append((root, "Minor Blues", "Parallel: Standard minor blues"))
            raw_suggestions.append((root, "Minor Pentatonic", "Parallel: Pure minor sound"))
        else:
            raw_suggestions.append((root, "Major Pentatonic", "Neutral: Bright and open"))

        # Package the final result, including a preview of the notes.
        results = []
        for s_root, s_type, reason in raw_suggestions:
            scale_notes = self._calculate_scale_notes(s_root, s_type)
            results.append({
                "name": f"{s_root} {s_type}",
                "reason": reason,
                "notes": scale_notes
            })
        return results

    def suggest_advanced(self, chord_input):
        """
        In addition to the basic recommendation, add an 'advanced alternative' pentatonic scale.
        For example, on Cmaj7, recommend G Major Pentatonic to obtain a #11 (Lydian) color.
        """
        converter = EnhancedChordConverter()
        notes = converter._ensure_notes_and_root(chord_input)
        root = notes[0]
        root_idx = converter.note_to_idx[root]
        chord_offsets = set([(converter.note_to_idx[n] - root_idx) % 12 for n in notes])
        
        recommendations = self.suggest_for_chord(chord_input) # Retrieve your existing basic recommendations

        # --- Adding advanced jazz pentatonic substitution logic ---
        # 1. Major 7th chord
        if 11 in chord_offsets:
            # Recommend the major pentatonic starting from the fifth (Cmaj7 play G Pent) -> yields 9, #11, 13
            g_root = converter.idx_to_note[(root_idx + 7) % 12]
            recommendations.append({
                "name": f"{g_root} Major Pentatonic",
                "reason": "Substitution: Provides Lydian (#11) color",
                "notes": self._calculate_scale_notes(g_root, "Major Pentatonic")
            })

        # 2. Minor 7th chord
        elif 3 in chord_offsets and 10 in chord_offsets:
            # Recommend the major pentatonic starting from the minor third (Am7 play C Pent) -> yields natural minor color
            b3_root = converter.idx_to_note[(root_idx + 3) % 12]
            recommendations.append({
                "name": f"{b3_root} Major Pentatonic",
                "reason": "Substitution: Smooth Aeolian texture",
                "notes": self._calculate_scale_notes(b3_root, "Major Pentatonic")
            })

        return recommendations
    
    def analyze_improv_feel(self, scale_notes, chord_notes):
        """
        Analyze the perceived style of a scale over a specific chord.
        scale_notes: List of notes in the recommended scale
        chord_notes: List of notes in the current chord
        """
        scale_set = set(scale_notes)
        chord_set = set(chord_notes)
        
        # 1. Identify the 'tension notes' in the scale (notes not in the chord)
        tensions = scale_set - chord_set
        # 2. Calculate the tension ratio
        tension_score = len(tensions)
        
        # 3. Rating logic
        if tension_score <= 1:
            feeling = "Safe & Sweet"
            description = "Consonant sound, perfect for pop and folk blues."
        elif tension_score <= 3:
            feeling = "Soulful & Balanced"
            description = "Classic blues feel with a good balance of tension and release."
        elif tension_score <= 5:
            feeling = "Spicy & Jazzy"
            description = "High tension, characteristic of bebop and modern jazz blues."
        else:
            feeling = "Experimental / Outside"
            description = "Very crunchy, creates strong dissonant colors."

        return {
            "feeling": feeling,
            "spiciness_level": tension_score,
            "description": description,
            "tension_notes": list(tensions)
        }

    def suggest_with_feel(self, chord_input):
        """Complete recommendation with perceptual analysis"""
        converter = EnhancedChordConverter()
        notes = converter._ensure_notes_and_root(chord_input) #
        root = notes[0]
        
        # Assume here we recommend several different styles.
        suggestions = [
            (root, "Major Pentatonic"),
            (root, "Minor Blues"),
            (root, "Lydian Dominant")
        ]
        
        report = []
        for s_root, s_name in suggestions:
            if s_name in self.scale_metadata:
                s_notes = self._calculate_scale_notes(s_root, s_name)
                feel = self.analyze_improv_feel(s_notes, notes)
                report.append({
                    "scale": f"{s_root} {s_name}",
                    "notes": s_notes,
                    "feel": feel
                })
        return report

class CSTAnalyzer:
    def __init__(self):
        self.handle_notes = {
            "Cb": "B",
            "C#": "Db",
            "D#": "Eb",
            "E#": "F",
            "Fb": "E",
            "F#": "Gb",
            "G#": "Ab",
            "A#": "Bb",
            "B#": "C",
        }
        self.notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        self.note_to_val = {n: i for i, n in enumerate(self.notes)}
        
        self.circle_of_fifths = ['Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F', 'C', 'G', 'D', 'A', 'E', 'B']
        
        # Define the semitone structure of the scale (0 represents the root)
        self.scale_definitions = {
        # --- Modes of Major ---
            "Ionian (Major)": [0, 2, 4, 5, 7, 9, 11],
            "Dorian": [0, 2, 3, 5, 7, 9, 10],
            "Phrygian": [0, 1, 3, 5, 7, 8, 10],
            "Lydian": [0, 2, 4, 6, 7, 9, 11],
            "Mixolydian": [0, 2, 4, 5, 7, 9, 10],
            "Aeolian (Minor)": [0, 2, 3, 5, 7, 8, 10],
            "Locrian": [0, 1, 3, 5, 6, 8, 10],

            # --- Variations ---
            "Neapolitan Major": [0, 1, 3, 5, 7, 9, 11],
            "Harmonic Major": [0, 2, 4, 5, 7, 8, 11],
            "Melodic Major (Asc)": [0, 2, 4, 5, 7, 9, 11], # Same as Ionian
            "Melodic Major (Desc)": [0, 2, 4, 5, 7, 8, 10], # Common in jazz IVm
            "Neapolitan Minor": [0, 1, 3, 5, 7, 8, 11],
            "Harmonic Minor": [0, 2, 3, 5, 7, 8, 11],
            "Melodic Minor": [0, 2, 3, 5, 7, 9, 11],
            "Phrygian Dominant": [0, 1, 4, 5, 7, 8, 10], # Flamenco / Phrygian Dominant
            "Altered (Super Locrian)": [0, 1, 3, 4, 6, 8, 10],
            "Lydian Dominant": [0, 2, 4, 6, 7, 9, 10],
            "Lydian Augmented": [0, 2, 4, 6, 8, 9, 11],
            
            # --- Other ---
            "Diminished (H-W)": [0, 1, 3, 4, 6, 7, 9, 10],
            "Dominant Diminished (W-H)": [0, 2, 3, 5, 6, 8, 9, 11],
            "Whole Tone": [0, 2, 4, 6, 8, 10],
            "Blues Major": [0, 3, 5, 6, 7, 10],
            "Blues Minor": [0, 2, 3, 4, 7, 9],
            "Bebop Dominant": [0, 2, 4, 5, 7, 9, 10, 11],
            "Bebop Major": [0, 2, 4, 5, 7, 8, 9, 11],

            # --- Traditional ---
            "Gong Mode (Gong)": [0, 2, 4, 7, 9],
            "Shang Mode (Shang)": [0, 2, 5, 7, 10],
            "Jue Mode (Jue)": [0, 3, 5, 8, 10],
            "Zhi Mode (Zhi)": [0, 2, 5, 7, 9],
            "Yu Mode (Yu)": [0, 3, 5, 7, 10],
            
            "Japan Major (Hirajoshi variant)": [0, 1, 5, 7, 10],
            "Japan Minor (Iwato)": [0, 2, 3, 7, 8],
            "Hungarian Minor": [0, 2, 3, 6, 7, 8, 11],
            "Egypt Scale": [0, 1, 3, 4, 7, 8, 10]
        }

    def scale_notes(self, *args):
        """
        Two calling methods are supported:
        1. finder.scale_notes("C Lydian")
        2. finder.scale_notes("C", "Lydian")
        """
        if len(args) == 1:
            # Handle 'C Lydian' string format
            root, scale_name = args[0].split(" ", 1)
        else:
            # Handle 'C', 'Lydian' two-parameter format
            root, scale_name = args[0], args[1]
        
        # Get the offset values from your dictionary
        if scale_name not in self.scale_definitions:
            raise ValueError(f"Scale {scale_name} not found in library")
            
        intervals = self.scale_definitions[scale_name]
        return tuple(self.get_scale_notes(root, intervals))
        
    def _get_relative_fifths_pos(self, root, note):
        """Calculate the number of steps note is displaced from root on the circle of fifths"""
        r = self.handle_notes.get(root, root)
        n = self.handle_notes.get(note, note)
        r_idx = self.circle_of_fifths.index(r)
        n_idx = self.circle_of_fifths.index(n)
        
        # 计算最短路径位移
        diff = n_idx - r_idx
        return diff

    def get_scale_notes(self, root, intervals):
        """Calculate the notes in the scale based on the root and intervals"""
        root_idx = self.notes.index(root)
        return set(self.notes[(root_idx + i) % 12] for i in intervals)

    def analyze_tensions(self, chord_notes : list, scale_full_name: str):
        """
        Input: [0,3,7], "C Ionian (Major)"
        Output: { "available": ["D", "A"], "avoid": ["F"] }
        """
        scale_notes = self.scale_notes(scale_full_name)
        
        # Convert notes to semitone indices for distance calculation
        chord_vals = [self.note_to_val[self.handle_notes.get(n, n)] for n in chord_notes]
        
        results = {"tensions": [], "avoid": []}
        
        for s_note in scale_notes:
            if s_note in chord_notes:
                continue  # Skip chord tones
                
            s_val = self.note_to_val[self.handle_notes.get(s_note, s_note)]
            is_avoid = False
            
            for c_val in chord_vals:
                # Core rule: Scale note is 1 semitone above chord tone (minor second dissonance)
                if (s_val - c_val) % 12 == 1:
                    is_avoid = True
                    break
            
            if is_avoid:
                results["avoid"].append(s_note)
            else:
                results["tensions"].append(s_note)
                
        return results

    def calculate_brightness(self, root: str, scale_notes: tuple):
        """
        Calculate brightness based on circle of fifths offset from the root
        Lydian's #4 yields positive values, Phrygian's b2 yields negative values
        """
        total_rel_pos = 0
        has_major_3rd = False
        
        root_val = self.note_to_val[self.handle_notes.get(root, root)]
        
        for n in scale_notes:
            # 1. Calculate relative displacement on the circle of fifths
            total_rel_pos += self._get_relative_fifths_pos(root, n)
            
            # 2. Check if major third (4 semitones) is present
            n_val = self.note_to_val[self.handle_notes.get(n, n)]
            if (n_val - root_val) % 12 == 4:
                has_major_3rd = True

        # Base score: Average circle of fifths offset
        score = total_rel_pos / len(scale_notes)
        
        # Adjustment: If it's a major-type scale (contains major third), raise the overall brightness baseline
        if has_major_3rd:
            score += 5.0  
        
        return round(score, 2)

    def analyze_cst(self, chord_notes : list | set | tuple):
        """Find which scales in which keys contain these chord tones"""
        
        for note in chord_notes:
            if note in self.handle_notes:
                chord_notes[chord_notes.index(note)] = self.handle_notes[note]
            
        
        chord_set = set(chord_notes)
        results = []

        for root in self.notes:
            for scale_name, intervals in self.scale_definitions.items():
                scale_notes = self.get_scale_notes(root, intervals)
                # If the chord tones are a subset of the scale notes
                if chord_set.issubset(scale_notes):
                    results.append(f"{root} {scale_name}")
        
        return results

class LCCAnalyzer:
    def __init__(self):
        self.handle_notes = {
            "Cb": "B",
            "C#": "Db",
            "D#": "Eb",
            "E#": "F",
            "Fb": "E",
            "F#": "Gb",
            "G#": "Ab",
            "A#": "Bb",
            "B#": "C",
        }
        self.notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
        self.note_to_val = {n: i for i, n in enumerate(self.notes)}

        # Define the circle of fifths order (used for calculating gravitational distance)
        # Starting from Gb to B, covering all 12 semitones in the circle of fifths
        self.fifths_order = ['Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F', 'C', 'G', 'D', 'A', 'E', 'B']

        # LCC core scale definitions (based on parent Lydian modifications)
        self.lcc_scales = {
            "Lydian (Fundamental)": [0, 2, 4, 6, 7, 9, 11],
            "Lydian Augmented": [0, 2, 4, 6, 8, 9, 11],
            "Lydian Diminished": [0, 2, 3, 6, 7, 9, 11],
            "Lydian b7 (Dominant)": [0, 2, 4, 6, 7, 9, 10],
            "Aux. Augmented (Whole Tone)": [0, 2, 4, 6, 8, 10],
            "Aux. Diminished": [0, 1, 3, 4, 6, 7, 9, 10],
            "Aux. Dim. Blues": [0, 1, 3, 4, 6, 7, 9, 10]
        }

    def _get_fifths_distance(self, note1, note2):
        """Calculate the step distance between two notes on the circle of fifths (0-6)"""
        n1 = self.handle_notes.get(note1, note1)
        n2 = self.handle_notes.get(note2, note2)
        idx1 = self.fifths_order.index(n1)
        idx2 = self.fifths_order.index(n2)
        dist = abs(idx1 - idx2)
        return min(dist, 12 - dist)

    def scale_notes(self, *args):
        """
        Two calling methods are supported:
        1. finder.scale_notes("C Lydian (Fundamental)")
        2. finder.scale_notes("C", "Lydian (Fundamental)")
        """
        if len(args) == 1:
            # Handle string format "C Lydian (Fundamental)"
            # split(" ", 1) ensures only the first space is split, preserving spaces in the scale name
            parts = args[0].split(" ", 1)
            if len(parts) != 2:
                raise ValueError("Invalid input format. Please use 'root scale_name' format")
            parent, scale_name = parts[0], parts[1]
        elif len(args) == 2:
            # Handle two-parameter format ("C", "Lydian (Fundamental)")
            parent, scale_name = args[0], args[1]
        else:
            raise TypeError("scale_notes() takes 1 or 2 positional arguments")

        # Get the parent root note value
        p_val = self.note_to_val[parent]
        
        # Get offset values from your lcc_scales dictionary
        if scale_name not in self.lcc_scales:
            raise KeyError(f"Not found in LCC scale library: {scale_name}")
            
        intervals = self.lcc_scales[scale_name]
        
        # Return the converted note list
        return tuple([self.notes[(p_val + i) % 12] for i in intervals])

    def analyze_lcc(self, chord_notes: list | set | tuple):
        """Find potential parent Lydian scales for the given chord tones, and rank them by 'gravitational' distance on the circle of fifths"""
        processed_notes = []
        for note in chord_notes:
            processed_notes.append(self.handle_notes.get(note, note))
        
        chord_root = processed_notes[0]
        results = []

        for parent_key in self.notes:
            p_val = self.note_to_val[parent_key]
            for lcc_name, intervals in self.lcc_scales.items():
                scale_notes_vals = set([(p_val + i) % 12 for i in intervals])
                chord_vals = set([self.note_to_val[n] for n in processed_notes])
                
                if chord_vals.issubset(scale_notes_vals):
                    degree = (self.note_to_val[chord_root] - p_val) % 12
                    
                    # Calculate gravitational value: circle of fifths distance between parent Lydian and chord root
                    gravity = self._get_fifths_distance(parent_key, chord_root)
                    
                    results.append({
                        "parent": parent_key,
                        "scale": lcc_name,
                        "degree_from_parent": degree,
                        "gravity": gravity  # Smaller value = more Ingoing
                    })

        # Core logic: Sort in ascending order by gravitational value (circle of fifths distance)
        # Distance 0 means the chord root is the parent Lydian root (most stable)
        results.sort(key=lambda x: x['gravity'])
        return results
    
class NeoRiemannianToolkit:
    def __init__(self):
        self.converter = EnhancedChordConverter()
        self.formulas = self.converter.chord_formulas

    def get_Dn_transform(self, chord_input, chord_form : list | tuple | set = [0, 4, 7], n=1):
        """
        General Dn transformation algorithm
        n=1: D (IV degree)
        n=2: D2 (bVII degree/step from V to IV)
        n=3: D3 (bIII degree)
        """
        info = self.converter._ensure_notes_and_root(chord_input, True)
        root_offset = self.converter.note_to_idx[info["root"]]
        
        shift = (5 * n) % 12
        
        dn_indices = [(x + root_offset + shift) % 12 for x in chord_form]
        
        return {
            f"D{n}": {
                "chord": self.converter.identify_chord(dn_indices)['chord'],
                "notes": [self.converter.idx_to_note[i] for i in dn_indices],
                "offsets": dn_indices
            }
        }

    def get_triad_transform(self, chord_input):
        """
        Tone Network Diagram core PLRSNDD2 transformation + Augmented hub logic
        """
        info = self.converter._ensure_notes_and_root(chord_input, True)
        notes = info["notes"]
        quality = info["quality"]
        if len(notes) < 3: return None
        
        root_offset = info["offsets"][0]
        r, t, f = [self.converter.note_to_idx[n] for n in notes[:3]]
        
        is_major = quality in ["", "maj", "major", "M"]
        is_minor = quality in ["min", "m", "minor"]
        is_aug = quality == "aug"
        is_dim = quality == "dim"
        is_sus4 = quality == "sus4"
        is_sus2 = quality == "sus2"
        
        major_form = self.converter.chord_formulas["major"]
        minor_form = self.converter.chord_formulas["minor"]
        aug_form = self.converter.chord_formulas["aug"]
        dim_form = self.converter.chord_formulas["dim"]
        sus4_form = self.converter.chord_formulas["sus4"]
        sus2_form = self.converter.chord_formulas["sus2"]
        
        raw_ops = {}
        if is_dim:
            raw_ops["s1_r"] = [(x + root_offset - 1) % 12 for x in major_form]
            raw_ops["p1_t_p1_f"] = [(x + root_offset) % 12 for x in major_form]
            raw_ops["p1_f"] = [(x + root_offset) % 12 for x in minor_form]
            raw_ops["s2_r"] = [(x + root_offset + 3) % 12 for x in minor_form]
            
            raw_ops["dim"] = [(x + root_offset + 6) % 12 for x in dim_form]
            
        elif is_sus4:
            raw_ops["Resolve_P_Maj"] = [(x + root_offset) % 12 for x in major_form]
            raw_ops["Resolve_P_Min"] = [(x + root_offset) % 12 for x in minor_form]
            raw_ops["To_sus2"] = [(x + root_offset) % 12 for x in sus2_form]
            raw_ops["To_IV"] = [(x + root_offset + 5) % 12 for x in major_form]
            
        elif is_sus2:
            raw_ops["Resolve_P_Maj"] = [(x + root_offset) % 12 for x in major_form]
            raw_ops["Resolve_P_Min"] = [(x + root_offset) % 12 for x in minor_form]
            raw_ops["To_sus4"] = [(x + root_offset) % 12 for x in sus4_form]
            
            raw_ops["To_V"] = [(x + root_offset + 7) % 12 for x in major_form]
            
        elif is_aug:
            raw_ops["s1_f"] = [(x + root_offset) % 12 for x in major_form]
            raw_ops["s1_t"] = [(x + root_offset + 4) % 12 for x in major_form]
            raw_ops["s1_r"] = [(x + root_offset - 4) % 12 for x in major_form]
            raw_ops["p1_f"] = [(x + root_offset + 1) % 12 for x in minor_form]
            raw_ops["p1_t"] = [(x + root_offset + 1 + 4) % 12 for x in minor_form]
            raw_ops["p1_r"] = [(x + root_offset + 1 - 4) % 12 for x in minor_form]

        elif is_major:
            raw_ops.update({
                "P": [(x + root_offset) % 12 for x in minor_form], 
                "L": [(x + root_offset + 4) % 12 for x in minor_form],
                "R": [(x + root_offset - 3) % 12 for x in minor_form],
                "S": [(x + root_offset + 1) % 12 for x in minor_form], 
                "N": [(x + root_offset + 5) % 12 for x in minor_form],
                "ToAug": [(x + root_offset) % 12 for x in aug_form],
                "ToSus4": [(x + root_offset) % 12 for x in sus4_form],
                "ToSus2": [(x + root_offset) % 12 for x in sus2_form],
                "ToDim": [(x + root_offset + 1) % 12 for x in dim_form],
            })
            
            for n in range(1,7):
                raw_ops[f"D{n}"] = self.get_Dn_transform(chord_input, major_form, n)['D'+str(n)]['offsets']
        elif is_minor:
            raw_ops.update({
                "P": [(x + root_offset) % 12 for x in major_form], 
                "L": [(x + root_offset - 4) % 12 for x in major_form], 
                "R": [(x + root_offset + 3) % 12 for x in major_form],
                "S": [(x + root_offset - 1) % 12 for x in major_form], 
                "N": [(x + root_offset + 7) % 12 for x in major_form],
                "ToAug": [(x + root_offset - 1) % 12 for x in aug_form],
                "ToSus4": [(x + root_offset) % 12 for x in sus4_form],
                "ToSus2": [(x + root_offset) % 12 for x in sus2_form],
                "ToDim": [(x + root_offset) % 12 for x in dim_form],
            })
            
            for n in range(1,7):
                raw_ops[f"D{n}"] = self.get_Dn_transform(chord_input, minor_form, n)['D'+str(n)]['offsets']

        # Format the output
        final_results = {}
        for op, idxs in raw_ops.items():
            chord_name = self.converter.identify_chord(idxs)['chord']
            note_names = [self.converter.idx_to_note[i % 12] for i in idxs]
            final_results[op] = {"chord": chord_name, "notes": note_names}
            
        return final_results
    
    def _build(self, root_idx, quality):
        """Assist in constructing chord names"""
        root_name = self.converter.idx_to_note[root_idx % 12]
        q = quality if quality in self.formulas else ""
        return f"{root_name}{q}"
    
    def get_octatonic_neighbors(self, chord_input):
        """
        Octave Tower Cycle
        """
        info = self.converter._ensure_notes_and_root(chord_input, True)
        root = info["offsets"][0]
        q = self.converter.identify_chord(info["offsets"])['quality']
        
        neighbors = []
        
        if q == "m7b5":
            neighbors += [self._build(root, "m7"), self._build(root+3, "m7"), 
                          self._build(root-1, "maj7"), self._build(root, "dim7")]

        elif q == "dim7":
            neighbors.append(self._build(root - 6, "m7b5"))
            neighbors.append(self._build(root - 3, "m7b5"))
            neighbors.append(self._build(root + 0, "m7b5"))
            neighbors.append(self._build(root + 3, "m7b5"))
            
            neighbors.append(self._build(root - 1, "7"))
            neighbors.append(self._build(root - 4, "7"))
            neighbors.append(self._build(root + 2, "7"))
            neighbors.append(self._build(root + 5, "7"))

        elif q == "maj7":
            neighbors += [self._build(root, "7"), self._build(root+1, "m7b5")]

        elif q == "7":
            neighbors += [self._build(root-5, "dim7"), self._build(root, "m7"), 
                          self._build(root-3, "m7"), self._build(root, "maj7")]

        elif q == "m7":
            neighbors += [self._build(root, "7"), self._build(root - 3, "m7b5"), 
                          self._build(root, "m7b5"), self._build(root + 3, "7")]

        # Filter out itself and null values
        unique_results = []
        seen = set()
        for n in neighbors:
            if n != chord_input and n not in seen:
                unique_results.append(n)
                seen.add(n)
        return unique_results
    
    def get_geometric_neighbors(self, chord_input):
        """Complete query integrating Octave Tower and Tone Network Diagram"""
        target_info = self.converter._ensure_notes_and_root(chord_input, True)
        target_offsets = set(target_info["offsets"])
        
        results = {
            "Tonnetz_PLRSND": {},
            "Octatonic_Tower": [],
        }

        # Fill in Tonnetz transformations (if it's a triad)
        if len(target_offsets) == 3:
            results["Tonnetz_PLRSND"] = self.get_triad_transform(chord_input)

        if len(target_offsets) >= 4:
            octatonic = self.get_octatonic_neighbors(chord_input)
            results["Octatonic_Tower"] = octatonic

        candidates = []
        
        tonnetz = results["Tonnetz_PLRSND"]
        for __, info in tonnetz.items():
            candidates.append(info["chord"])
            
        # 遍历 Octatonic_Tower (列表结构)
        oct_tower = results["Octatonic_Tower"]
        for chord_name in oct_tower:
            candidates.append(chord_name)

        results["candidates"] = candidates

        return results
    
class JazzBrain:
    """Main class to integrate EnhancedChordConverter, BluesToolkit, CSTAnalyzer, and LCCAnalyzer for providing improvisation advice based on a given chord"""
    def __init__(self):
        self.converter = EnhancedChordConverter()
        self.cst = CSTAnalyzer()
        self.lcc = LCCAnalyzer()
        self.blues = BluesToolkit()
        self.nrt = NeoRiemannianToolkit()

    def get_advice(self, *args):
        """Given a chord string (e.g., 'G7', 'F#m7b5', 'Bbmaj9'), provide improvisation advice based on both CST and LCC analyses"""
        # 1. Parse notes
        chords_notes = []
        if isinstance(args[0], str):
            chord_str = args[0]
            chords_notes = self.converter._ensure_notes_and_root(chord_str)
        elif isinstance(args[0], list) or isinstance(args[0], set) or isinstance(args[0], tuple):
            chord_str = "Custom Chord"
            chords_notes = list(args[0])
          
       # 2. CST approach (sorted by brightness)
        cst_results = self.cst.analyze_cst(chords_notes) # Root must be provided to calculate relative brightness
        
        # 3. LCC approach (sorted by gravity)
        lcc_results = self.lcc.analyze_lcc(chords_notes)
        
        # 4. Output a human-readable report
        print(f"--- Suggested improv approaches for {chord_str} ---")
        advice_scale = cst_results[0]
        scale_notes = self.cst.scale_notes(advice_scale)
        chord_root = chords_notes[0]
        print(f"Most stable (CST): {advice_scale} (brightness: {self.cst.calculate_brightness(chord_root,scale_notes)})")
        print(f"Most modern (LCC): {lcc_results[0]['parent']} {lcc_results[0]['scale']} (gravity: {lcc_results[0]['gravity']})")
        
        
    # --- Chord Progression Analysis (Functional Analysis) ---
    def analyze_progression(self, progression: list):
        """Analyze chord progressions, identify ii-V-I and other functions"""
        results = []
        for i in range(len(progression)):
            current = progression[i]
            # Simple ii-V-I detection logic (based on root relationships)
            if i < len(progression) - 1:
                next_chord = progression[i+1]
                chords_root_current = self.converter._ensure_notes_and_root(current)[0]
                chords_root_next = self.converter._ensure_notes_and_root(next_chord)[0]
                
                # Get root note index
                r1 = self.converter.note_to_idx[chords_root_current]
                r2 = self.converter.note_to_idx[chords_root_next]
                
                if (r2 - r1) % 12 == 5: # Perfect fourth ascending / perfect fifth descending
                    results.append(f"{current} -> {next_chord}: Strong functional progression (Dominant Motion)")
        return results

    # --- Automatic voicing generator (Voicing Generator) ---
    def get_voicing(self, chord, v_type="shell"):
        """Generate voicings in a specific style"""
        notes = self.converter._ensure_notes_and_root(chord)
        
        if v_type == "shell":
            # Shell Voicing: Root + 3rd + 7th
            return [notes[0], notes[1], notes[2] if len(notes) > 2 else notes[-1]]
        
        if v_type == "drop2":
            # Drop 2: Lower the penultimate note of the sorted notes by one octave (simplified demonstration)
            if len(notes) >= 4:
                return [notes[-2], notes[0], notes[1], notes[-1]]
        return notes

    # --- Color substitution suggestions (Substitution) ---
    def get_substitutions(self, chord_input):
        """
        Suggest chord substitutions based on chord intervals.
        Supports both string (e.g., 'G7') and list (e.g., ['G', 'B', 'D', 'F']).
        """
        # 1. Uniformly parse notes and extract the root
        notes = self.converter._ensure_notes_and_root(chord_input)
        if not notes:
            return []
            
        root = notes[0]
        root_idx = self.converter.note_to_idx[root]
        
        # 2. Calculate the semitone offset relative to the root note for attribute determination
        offsets = set([(self.converter.note_to_idx[n] - root_idx) % 12 for n in notes])
        subs = []
        
        # Determine the characteristic notes
        has_major_3rd = 4 in offsets
        has_minor_3rd = 3 in offsets
        has_b7 = 10 in offsets
        has_maj7 = 11 in offsets

        # --- Tritone Substitution ---
        # Logic: Must contain a tritone (Dominant 7th characteristic: major third + minor seventh)
        if has_major_3rd and has_b7:
            tritone_root_idx = (root_idx + 6) % 12
            tritone_root = self.converter.idx_to_note[tritone_root_idx]
            subs.append({"name": f"{tritone_root}7", "type": "Tritone Sub"})
            
        # --- Relative Major/Minor Substitution ---
        # Logic: If it's a minor chord (contains a minor third), recommend its relative major
        if has_minor_3rd:
            rel_root_idx = (root_idx + 3) % 12
            rel_root = self.converter.idx_to_note[rel_root_idx]
            subs.append({"name": f"{rel_root}maj7", "type": "Relative Major Sub"})
            
        # Logic: If it's a major chord (contains a major third), recommend its relative minor.
        elif has_major_3rd:
            rel_root_idx = (root_idx - 3) % 12
            rel_root = self.converter.idx_to_note[rel_root_idx]
            subs.append({"name": f"{rel_root}m7", "type": "Relative Minor Sub"})
            
        return subs

    # --- Interactive Visualization (Visualizer) ---
    def draw_piano(self, notes: list):
        """Draw a simple piano keyboard in the terminal"""
        keyboard = ["  "] * 12
        note_indices = [self.converter.note_to_idx[n] for n in notes]
        
        for i in range(12):
            if i in note_indices:
                keyboard[i] = "●" # Indicates pressed notes
            else:
                keyboard[i] = "-"
        
        print("\nPiano Visualization:")
        print("C   C#  D   D#  E   F   F#  G   G#  A   A#  B ")
        print(" | ".join(keyboard))

    # --- Enhanced Advice ---
    def get_full_report(self, chord_str: str):
        print(f"=== {chord_str} Jazz Report ===")
        notes = self.converter._ensure_notes_and_root(chord_str)
        
        # Visualization
        self.draw_piano(notes)
        
        # Voicing Suggestions
        print(f"\n[Voicings]")
        print(f"Shell Voicing: {self.get_voicing(chord_str, 'shell')}")
        
        # Substitution Suggestions
        subs = self.get_substitutions(chord_str)
        if subs:
            print(f"\n[Substitutions]")
            for s in subs:
                print(f"Try {s['name']} ({s['type']})")
        
        # Original CST/LCC Logic
        self.get_advice(chord_str)
        
    # --- Key Center Analyzer ---
    def find_key_center(self, progression: list):
        """Find the most fitting key center for the entire progression"""
        all_notes = set()
        for c in progression:
            notes = self.converter._ensure_notes_and_root(c)
            if notes: 
                all_notes.update(notes)
        
        best_key = None
        max_overlap = -1
        
        # Iterate through all 12 major scales to find which one contains the most notes
        for root in self.cst.notes:
            scale_notes = self.cst.get_scale_notes(root, self.cst.scale_definitions["Ionian (Major)"])
            overlap = len(all_notes.intersection(scale_notes))
            if overlap > max_overlap:
                max_overlap = overlap
                best_key = root
        return f"{best_key} Major (Match Score: {max_overlap}/{len(all_notes)})"

    def find_key_center_pro(self, progression: list, return_all=False):
        """
        Final Professional Key Center Analysis.
        Focuses on functional resolution and specific chord quality roles.
        """
        all_notes = set()
        roots = []
        chord_names = []
        
        for c in progression:
            notes = self.converter._ensure_notes_and_root(c)
            root = notes[0] if notes else None
            if notes:
                all_notes.update(notes)
                roots.append(root)
                chord_names.append(c if isinstance(c, str) else "")

        # 1. Parent Systems with priorities
        systems_config = {
            "Major (Ionian)": ([0, 2, 4, 5, 7, 9, 11], 2.5), # Highest priority
            "Jazz Minor (Melodic)": ([0, 2, 3, 5, 7, 9, 11], 2.0),
            "Harmonic Minor": ([0, 2, 3, 5, 7, 8, 11], 1.5),
            "Harmonic Major": ([0, 2, 4, 5, 7, 8, 11], 1.2),
            "Diminished (H-W)": ([0, 1, 3, 4, 6, 7, 9, 10], 0.5),
            "Whole Tone": ([0, 2, 4, 6, 8, 10], 0.5)
        }

        all_results = []
        for key_root in self.cst.notes:
            key_idx = self.converter.note_to_idx[key_root]
            
            for sys_name, (intervals, priority) in systems_config.items():
                scale_notes = self.cst.get_scale_notes(key_root, intervals)
                
                # --- Base matching score ---
                score = len(all_notes.intersection(scale_notes)) + priority
                
                # --- Functional Weighting ---
                for i, r in enumerate(roots):
                    rel_idx = (self.converter.note_to_idx[r] - key_idx) % 12
                    actual = chord_names[i].lower()
                    
                    # C Major specific check for Dm7 -> G7
                    if sys_name == "Major (Ionian)":
                        # ii-V resolution check
                        if rel_idx == 2 and "m" in actual: score += 4.0 # Correct iim7
                        if rel_idx == 7 and "7" in actual and "maj" not in actual: 
                            # If G7 is at the end, it's likely a V7 pointing to I
                            if i == len(roots) - 1: score += 5.0 
                            else: score += 2.0
                        if rel_idx == 0 and "maj" in actual: score += 4.0 # Correct Imaj7
                
                # --- Penalty for G Major misinterpretation ---
                if sys_name == "Major (Ionian)" and key_root == roots[-1] and "7" in chord_names[-1]:
                    # A dominant 7th as the final chord is ALMOST NEVER the Tonic (I).
                    # It's usually the V7. Penalize this key as being the root.
                    score -= 10.0

                # --- The Third Rule (Hard constraint) ---
                has_minor_3rd = self.converter.idx_to_note[(key_idx + 3) % 12] in all_notes
                has_major_3rd = self.converter.idx_to_note[(key_idx + 4) % 12] in all_notes
                if (4 in intervals) and has_minor_3rd and not has_major_3rd: score -= 15.0
                if (3 in intervals) and has_major_3rd and not has_minor_3rd: score -= 15.0

                all_results.append({"name": f"{key_root} {sys_name}", "score": round(score, 2)})

        all_results.sort(key=lambda x: x["score"], reverse=True)
        return all_results if return_all else f"Recommended Key: {all_results[0]['name']}"
    
    # --- Guide Tones ---
    def get_guide_tone_path(self, progression: list):
        """Calculate the 3rd and 7th voice leading paths between chords"""
        path = []
        for c in progression:
            notes = self.converter._ensure_notes_and_root(c)
            if len(notes) >= 3:
                # Jazz guide tones are usually the 2nd and 4th notes (the 3rd and 7th)
                guide = [notes[1], notes[3] if len(notes) > 3 else notes[-1]]
                path.append(guide)
        return path
    
    # --- Negative Harmony ---
    def to_negative(self, chord_input, axis="C"):
        """Mirror the chord across the circle of fifths axis (default C-G axis)"""
        # Core logic: Based on the C-G axis, mapping relationships are C→G, G→C, D→F, F→D, etc.
        # In the chromatic scale, the C-G axis center point is 3.5 (between E and Eb)
        axis_val = self.converter.note_to_idx[axis] + 3.5
        notes = self.converter._ensure_notes_and_root(chord_input)
        
        neg_notes = []
        for n in notes:
            val = self.converter.note_to_idx[n]
            # Mirror formula: new_val = 2 * axis - original_val
            neg_val = int((2 * axis_val - val) % 12)
            neg_notes.append(self.converter.idx_to_note[neg_val])
        return neg_notes
    
    def get_chord_recommendations(self, chord_input):
        curr_info = self.converter._ensure_notes_and_root(chord_input, True)
        curr_root = curr_info["offsets"][0]
        curr_notes_set = frozenset(curr_info["offsets"])
        
        raw_candidates = []
        seen_structures = {curr_notes_set} # Used for deduplicating physical notes

        # 1. Extract all unique formula structures (deduplication logic)
        unique_formulas = {}
        for f_name, f_offsets in self.converter.chord_formulas.items():
            f_set = frozenset(f_offsets)
            if f_set not in unique_formulas:
                unique_formulas[f_set] = f_name

        # 2. Iterate through all 12 roots, generating all possible formula chords
        for r_offset in range(12):
            root_name = self.converter.idx_to_note[r_offset]
            for f_set, f_name in unique_formulas.items():
                # Convert to absolute semitone indices
                abs_offsets = tuple(sorted([(x + r_offset) % 12 for x in f_set]))
                abs_fset = frozenset(abs_offsets)
                
                if abs_fset not in seen_structures:
                    stability = self._calculate_stability(curr_notes_set, abs_fset)
                    # Keep only chords with certain relevance to avoid completely random noise
                    if stability > 3.0:
                        raw_candidates.append({
                            "chord": f"{root_name}{f_name}",
                            "source": "Formula",
                            "offsets": abs_offsets, # Store the sorted tuple here to resolve indexing issues
                            "root": r_offset,       # Explicitly store the root note
                            "stability": stability
                        })
                        seen_structures.add(abs_fset)

        # 3. Dynamically created chords (Mutation: Add/Omit)
        mutations = []
        # Mutate the top 15 most stable candidates
        for cand in sorted(raw_candidates, key=lambda x: x['stability'], reverse=True)[:15]:
            c_root = cand['root']
            c_offsets = list(cand['offsets'])
            
            # --- Mutation A: Omit 5 (Core of jazz, removing the perfect fifth creates more transparent voicings) ---
            # Check for the presence of a perfect fifth (offset 7 relative to the root)
            fifth_val = (c_root + 7) % 12
            if fifth_val in c_offsets:
                no5_offsets = tuple(sorted([n for n in c_offsets if n != fifth_val]))
                if frozenset(no5_offsets) not in seen_structures:
                    mutations.append({
                        "chord": f"{cand['chord']}(no5)",
                        "source": "Creative(Omit)",
                        "offsets": no5_offsets,
                        "root": c_root,
                        "stability": self._calculate_stability(curr_notes_set, frozenset(no5_offsets))
                    })
                    seen_structures.add(frozenset(no5_offsets))

            # --- Mutation B: Add 9 / Add 11 (Add color) ---
            for ext_interval in [2, 5]: # 9th, 11th
                ext_val = (c_root + ext_interval) % 12
                if ext_val not in c_offsets:
                    ext_offsets = tuple(sorted(c_offsets + [ext_val]))
                    if frozenset(ext_offsets) not in seen_structures:
                        label = "add9" if ext_interval == 2 else "add11"
                        mutations.append({
                            "chord": f"{cand['chord']}{label}",
                            "source": "Creative(Add)",
                            "offsets": ext_offsets,
                            "root": c_root,
                            "stability": self._calculate_stability(curr_notes_set, frozenset(ext_offsets))
                        })
                        seen_structures.add(frozenset(ext_offsets))

        raw_candidates.extend(mutations)

        final_results = []
        for item in raw_candidates:
            # 1. Basic physical indicators
            stability = self._calculate_stability(curr_notes_set, item['offsets'])
            brightness = self._calculate_brightness(curr_root, item['root'], item['offsets'])
            
            # 2. Calculate tension value [0-10]
            tension = self._calculate_tension(item['root'], item['offsets'], item['source'])
            
            # Comprehensive recommendation score (Score) algorithm upgrade
            # Score = Stability balance + Tension reward (moderate)
            # We don't want the score to only favor stable chords; chords with tension that also lead somewhere are the interesting ones
            rec_score = (stability * 0.6) + (tension * 0.4) 
            
            # Common tone reward
            common_count = len(curr_notes_set.intersection(item['offsets']))
            rec_score += (common_count * 0.2)
            
            final_results.append({
                "chord": item["chord"],
                "source": item["source"],
                "score": round(max(0, min(10, rec_score)), 1),
                "stability": stability,
                "tension": tension,
                "brightness": brightness,
                "notes": [self.converter.idx_to_note[n] for n in item["offsets"]]
            })

        # Sorting: Prioritize total score, showcasing the most musical connections
        final_results.sort(key=lambda x: x["score"], reverse=True)
        return final_results

    def _calculate_tension(self, root, offsets, source):
        """
        Calculate tension value:
        - Contains tritone: +3.0
        - Contains minor second (m2): +2.5 (extremely high tension)
        - Contains major seventh (M7): +1.5
        - Each extension (9, 11, 13): +1.0
        - Mutation source compensation: +1.0
        """
        tension = 0.0
        # Convert to intervals relative to the root
        intervals = sorted([(n - root) % 12 for n in offsets])
        
        # 1. Internal interval conflict detection
        for i in range(len(intervals)):
            for j in range(i + 1, len(intervals)):
                diff = abs(intervals[i] - intervals[j]) % 12
                if diff == 6: tension += 3.0    # Tritone
                if diff == 1: tension += 2.5    # Small Second
                if diff == 11: tension += 1.5   # Major Seventh

        # 2. Extension note richness
        extensions = [n for n in intervals if n in [1, 2, 5, 6, 8, 10]] # b9, 9, 11, #11, b13, 13
        tension += len(extensions) * 0.8

        # 3. Source bonus
        if source.startswith("Creative"): tension += 1.0
        if source == "Negative": tension += 1.5 # Negative harmony typically carries a mysterious tension

        return round(max(0, min(10, tension)), 1)

    def _calculate_stability(self, set1, set2):
        """Calculate voice-leading stability"""
        common = len(set1.intersection(set2))
        dist = 0
        for n1 in set1:
            dist += min([abs(n1 - n2) % 12 for n2 in set2])
        return round(10 - (dist * 0.8) + (common * 2.0), 1)

    def _calculate_brightness(self, curr_root, next_root, next_offsets):
        """Calculate brightness based on circle of fifths displacement and interval qualities"""
        def get_circle_pos(idx): return (idx * 7) % 12
        
        shift = (get_circle_pos(next_root) - get_circle_pos(curr_root) + 6) % 12 - 6
        
        # Quality bonus: Check for inclusion of bright intervals such as major thirds and major sevenths
        bias = 0
        rel_notes = [(n - next_root) % 12 for n in next_offsets]
        if 4 in rel_notes: bias += 1  # Major third bright
        if 3 in rel_notes: bias -= 2  # Minor third dark
        if 11 in rel_notes: bias += 1 # Major seventh bright
        if 6 in rel_notes: bias -= 1  # Tritone unstable/dark
        if 2 in rel_notes: bias += 1  # Ninth bright
        
        return int(max(-10, min(10, shift + bias)))
    
    # --- Rhythmic Comping ---
    def get_rhythmic_voicing(self, chord_input, style="Charleston"):
        """Generate rhythmic syncopation for chords"""
        notes, _ = self.converter._ensure_notes_and_root(chord_input)
        # Simple Shell Voicing extraction
        v = [notes[0], notes[1], notes[2] if len(notes) > 2 else notes[-1]]
        
        styles = {
            "Charleston": [("1", v), ("1.5.offbeat", v)], # Offbeats after beat 1 and beat 2
            "Four_on_the_floor": [("1", v), ("2", v), ("3", v), ("4", v)]
        }
        return styles.get(style, styles["Charleston"])