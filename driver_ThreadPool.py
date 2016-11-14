import sncosmo
from analyzeSN import SNANASims
from analyzeSN import ResChar
import numpy as np
from datetime import datetime
from multiprocessing.dummy import Pool as ThreadPool
execfile('options.py')

num_threads = 4
num_sn = 6

begin_time = datetime.now()

def writeElapsedTime(num_failed) :
    elapsed_time = datetime.now() - begin_time
    output = ( '\n' + __file__ + ', ' + str(elapsed_time.total_seconds())
               + ', ' + str(num_sn) + ', ' + str(num_failed) + ', '
               + str(num_threads) )
    with open('benchmarks', 'a') as f:
        f.write(output)

def inferParams(snanaSims, model, infer_method, i, minsnr=3.):
    """
    infer the parameters for the ith supernova in the simulation
    """
    try :
        snid = snanaSims.headData.index.values[i]
        z = snanaSims.headData.ix[snid, 'REDSHIFT_FINAL']
        lcinstance = snanaSims.get_SNANA_photometry(snid=snid)
        model.set(z=z)
        print(z)
        resfit = infer_method(lcinstance.snCosmoLC(), model,
                              vparam_names=['t0', 'x0', 'x1', 'c'],
                              modelcov=True, minsnr=minsnr)
        return snid, ResChar.fromSNCosmoRes(resfit)
    except:
        return snid, None

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
    pool = ThreadPool(num_threads)
    results = pool.map(lambda x : inferParams(snana_eg, model,
                                              sncosmo.fit_lc,
                                              x, minsnr=3.)
                       , range(num_sn) )
    fh = open('results.dat', 'w') # Should Not be a text file when improved!
    i = 0
    failed_sn = 0
    while results :
        snid, r = results.pop()
        if r is not None :
            write_str = snid
            write_str += ','.join(map(str, r.parameters)) 
            # We should only keep the the independent components
            # unlike what I am doing here
            write_str += ','.join(map(str, np.asarray(r.covariance).flatten().tolist()))
            fh.write(write_str)
        else:
            print('SN {} failed'.format(i))
            failed_sn += 1
        i+=1
    fh.close()
    writeElapsedTime(failed_sn)
