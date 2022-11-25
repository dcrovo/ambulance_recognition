from detector.detector_for_desktop import parse, AmbulanceDetection

args = parse()
detector = AmbulanceDetection(args)
detector.run()