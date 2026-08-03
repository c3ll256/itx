import objc, Foundation, AppKit, sys
objc.loadBundle('Vision', globals(), bundle_path='/System/Library/Frameworks/Vision.framework')
objc.loadBundle('CoreImage', globals(), bundle_path='/System/Library/Frameworks/CoreImage.framework')
for path in sys.argv[1:]:
  url=Foundation.NSURL.fileURLWithPath_(path)
  data=Foundation.NSData.dataWithContentsOfURL_(url)
  ci=CIImage.imageWithData_(data)
  print('ci',ci, 'extent',ci.extent())
  req=VNRecognizeTextRequest.alloc().init()
  req.setRecognitionLevel_(0) # accurate? enum 0 accurate perhaps
  req.setUsesLanguageCorrection_(False)
  req.setMinimumTextHeight_(0.005)
  print('rev',req.revision())
  handler=VNImageRequestHandler.alloc().initWithCIImage_options_(ci,{})
  ok=handler.performRequests_error_([req],None)
  print('ok',ok,'results',req.results())
  for o in req.results() or []:
   cs=o.topCandidates_(3)
   print([(c.string(),c.confidence()) for c in cs], o.boundingBox())
