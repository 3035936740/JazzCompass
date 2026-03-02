from jazz_compass import ChordConverter, CSTAnalyzer, LCCAnalyzer, JazzBrain, BluesToolkit

if __name__ == "__main__":
    # --- Test Run ---
    converter = ChordConverter()

    # Test different input formats
    tests = ["Gmaj", "G#", "Gb", "Gb7", "Cm7", "A#sus4", "D", "D/C", "C/G", "F#dim7/E", "Bbmaj7", "E7b9"]

    for t in tests:
        res = converter.parse_and_get_notes(t)
        if isinstance(res, dict):
            print(res)
        else:
            print(res)
    # --- example ---
    finder = CSTAnalyzer()

    # Define C7 chord tones: C, E, G, Bb
    C7 = converter.parse("C7/E")

    print(f"--- Scales containing {C7} ---")
    matching_scales = finder.analyze_cst(C7)

    for scale in matching_scales:
        print(f"✔ {scale}")
        notes = finder.scale_notes(scale)
        print("Scale notes:",notes, "Brightness", finder.calculate_brightness(C7[0],notes))
        print(finder.analyze_tensions(C7, scale))
    
    print("--- LCC Theory Analysis Results ---")
    
    finder = LCCAnalyzer()
    
    c7_match = finder.analyze_lcc(C7)
    for m in c7_match:
        # According to LCC logic, the most typical parent for C7 is F Lydian b7
        # Because C is the dominant (V) of F
        print(f"Parent Lydian: {m['parent']:2} | Derived Scale: {m['scale']:25} | Relative Position: {m['degree_from_parent']} semitones | Gravity: {m['gravity']}")
        scale = f"{m['parent']} {m['scale']}"
        print(finder.scale_notes(scale))
        
    jazz_brain = JazzBrain()
    jazz_brain.get_advice(C7)
    jazz_brain.get_full_report("C7")
    
    analyze_progression = ["Cmaj7",["F", "A", "C", "E"], "G7", "Cmaj7"] # ["F", "A", "C", "E"] is Fmaj7 in note list format
    print(f"\n--- Analyzing Progression: {' - '.join([str(c) if isinstance(c, (list, set, tuple)) else c for c in analyze_progression])} ---")
    print(jazz_brain.analyze_progression(analyze_progression))
    
    print("\n--- Guide Tone Lines for Progression ---")
    prog = ["Dm7", "G7", "Cmaj7"]

    print("Tonal Center / Key Center:", jazz_brain.find_key_center(prog))

    print("Negative Harmony Dm7:", jazz_brain.to_negative("Dm7"))

    print("Guide Tone Line:", jazz_brain.get_guide_tone_path(prog))

    custom_chord = ["D", "F", "A", "C"]
    print("Custom Chord Transformation:", jazz_brain.to_negative(custom_chord))
    
    print(f"--- Passing Diminished ---")
    test_1 = ["Cmaj7", "Ebdim7", "Dm7", "G7"]
    print(jazz_brain.find_key_center_pro(test_1))
    
    jazz_minor_test = ["Cm6", "F7", "Bbmaj7"]
    print(jazz_brain.find_key_center_pro(jazz_minor_test))
    
    diminished_test = ["Bdim7", "Ddim7", "Fdim7", "Abdim7"]
    print(jazz_brain.find_key_center_pro(diminished_test))
    
    whole_tone_test = ["G7#5", "A7#5", "B7#5"]
    print(jazz_brain.find_key_center_pro(whole_tone_test))
    
    harmonic_minor_test = ["Am(maj7)", "E7b9", "Am6"]
    print(jazz_brain.find_key_center_pro(harmonic_minor_test))

    blues = BluesToolkit()
    sug = blues.suggest_for_chord("C7")
    print(f"----- C7 -----")
    print(sug)
    sug2 = blues.suggest_advanced(['C', 'E', 'G', 'B'])
    print(f"----- ['C', 'E', 'G', 'B'] -----")
    print(sug2)

    chord = 'G7'
    results = blues.suggest_with_feel(chord)

    print("\n--- Improvisation Feel Report ---")
    for r in results:
        f = r['feel']
        print(f"Scale: {r['scale']}")
        print(f"  Notes: {r['notes']}")
        print(f"  Feel : {f['feeling']} (Spiciness: {f['spiciness_level']})")
        print(f"  Info : {f['description']}")
        print(f"  Tension Source: {f['tension_notes']}")
        print("-" * 40)