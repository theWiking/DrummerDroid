import scripts.single.signatur_maker as SignatureMaker
import matplotlib.pyplot as plt
import resource

sm = SignatureMaker.Signature(resource.ROOT_DIR+'/date/audio/0.wav')
#plt.plot(s)
sm.fft_signature()
sm.save_signature('test.jpg')
#plt.show()