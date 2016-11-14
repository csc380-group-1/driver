import sncosmo
from analyzeSN import SNANASims
from analyzeSN import ResChar
import numpy as np
from datetime import datetime
import threading
execfile('options.py')

begin_time = datetime.now()

def writeElapsedTime() :
    elapsed_time = datetime.now() - begin_time
    output = ( '\n' + __file__ + ', ' + str(elapsed_time.total_seconds())
               + ', 3' )
    with open('benchmarks', 'a') as f:
        f.write(output)

### thread for inferParams1

def inferParams1(snanaSims1, model1, infer_method1, i, minsnr=3.):
    """
    infer the parameters for the ith supernova in the simulation
    """
    snid1 = snanaSims1.headData.index.values[i]
    z1 = snanaSims1.headData.ix[snid1, 'REDSHIFT_FINAL']
    lcinstance = snanaSims1.get_SNANA_photometry(snid=snid1)
    model1.set(z=z1)
    print(z1)
    resfit1 = infer_method1(lcinstance.snCosmoLC(), model1, vparam_names=['t0', 'x0', 'x1', 'c'],
                          modelcov=True, minsnr=minsnr)
    reschar1 = ResChar.fromSNCosmoRes(resfit1)
    return snid1, reschar1

### Thread for inferParam2

def inferParams2(snanaSims2, model2, infer_method2, i, minsnr=3.):
    """
    infer the parameters for the ith supernova in the simulation
    """
    snid2 = snanaSims2.headData.index.values[i]
    z2 = snanaSims2.headData.ix[snid2, 'REDSHIFT_FINAL']
    lcinstance = snanaSims2.get_SNANA_photometry(snid=snid2)
    model2.set(z=z2)
    print(z2)
    resfit2 = infer_method2(lcinstance.snCosmoLC(), model2, vparam_names=['t0', 'x0', 'x1', 'c'],
                          modelcov=True, minsnr=minsnr)
    reschar2 = ResChar.fromSNCosmoRes(resfit2)
    return snid2, reschar2
    
##### Thread for inferParam3


def inferParams3(snanaSims3, model3, infer_method3, i, minsnr=3.):
    """
    infer the parameters for the ith supernova in the simulation
    """
    snid3 = snanaSims3.headData.index.values[i]
    z3 = snanaSims3.headData.ix[snid3, 'REDSHIFT_FINAL']
    lcinstance = snanaSims3.get_SNANA_photometry(snid=snid3)
    model3.set(z=z3)
    print(z3)
    resfit3 = infer_method3(lcinstance.snCosmoLC(), model3, vparam_names=['t0', 'x0', 'x1', 'c'],
                          modelcov=True, minsnr=minsnr)
    reschar3 = ResChar.fromSNCosmoRes(resfit3)
    return snid3, reschar3   
   
   
### Create the variables which are the same for all threads    
    
snana_eg = SNANASims.fromSNANAfileroot(snanafileroot='LSST_Ia',
                                       location=minion_filepath,
                                       coerce_inds2int=False)

if __name__ == '__main__':
    snana_eg = SNANASims.fromSNANAfileroot(snanafileroot='LSST_Ia',
                                           location=minion_filepath,
                                           coerce_inds2int=False)
    dust = sncosmo.CCM89Dust()
    model = sncosmo.Model(source='salt2-extended',
		          effects=[dust, dust],
                          effect_names=['host', 'mw'],
		          effect_frames=['rest', 'obs'])
		          
#### create thread1		          
		          
def thread1():
		          
	try:
		snid1, r1 = inferParams1(snana_eg, model, sncosmo.fit_lc, 0, minsnr=3.)
		with open('results.dat', 'w') as fh: # Should Not be a text file when improved!
			write_str1 = snid1
			write_str1 += ','.join(map(str, r1.parameters)) 
				# We should only keep the the independent components
				# unlike what I am doing here
			write_str1 += ','.join(map(str, np.asarray(r1.covariance).flatten().tolist()))
			fh.write(write_str1)
	except:
		print('SN {} failed'.format(0))
		
		
### Create thread2		
		
def thread2():
		          
	try:
		snid2, r2 = inferParams2(snana_eg, model, sncosmo.fit_lc, 1, minsnr=3.)
		with open('results.dat', 'w') as fh: # Should Not be a text file when improved!
			write_str2 = snid2
			write_str2 += ','.join(map(str, r2.parameters)) 
				# We should only keep the the independent components
				# unlike what I am doing here
			write_str2 += ','.join(map(str, np.asarray(r2.covariance).flatten().tolist()))
			fh.write(write_str2)
	except:
		print('SN {} failed'.format(1))
		
		
		
##### create thread3		
		
def thread3():
		          
	try:
	
		snid3, r3 = inferParams3(snana_eg, model, sncosmo.fit_lc, 2, minsnr=3.)
		
		with open('results.dat', 'w') as fh: # Should Not be a text file when improved!
			write_str3 = snid3
			write_str3 += ','.join(map(str, r3.parameters)) 
				# We should only keep the the independent components
				# unlike what I am doing here
			write_str3 += ','.join(map(str, np.asarray(r3.covariance).flatten().tolist()))
			fh.write(write_str3)
	except:
		print('SN {} failed'.format(2))
		
		
		
###### initiate the threads		
	
t1 = threading.Thread(target = thread1)

t2 = threading.Thread(target = thread2)
t3 = threading.Thread(target = thread3)

t1.start()

t2.start()

t3.start()
t1.join()
t2.join()
t3.join()

writeElapsedTime()
