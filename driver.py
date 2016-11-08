import sncosmo
from analyzeSN import SNANASims
from analyzeSN import ResChar
import numpy as np
execfile('options.py')

def inferParams(snanaSims, model, infer_method, i, minsnr=3.):
    """
    infer the parameters for the ith supernova in the simulation
    """
    snid = snanaSims.headData.index.values[i]
    z = snanaSims.headData.ix[snid, 'REDSHIFT_FINAL']
    lcinstance = snanaSims.get_SNANA_photometry(snid=snid)
    model.set(z=z)
    print(z)
    resfit = infer_method(lcinstance.snCosmoLC(), model, vparam_names=['t0', 'x0', 'x1', 'c'],
                          modelcov=True, minsnr=minsnr)
    reschar = ResChar.fromSNCosmoRes(resfit)
    return snid, reschar

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
    for i in range(3):
	try:
	    snid, r = inferParams(snana_eg, model, sncosmo.fit_lc, i, minsnr=3.)
	    with open('results.dat', 'w') as fh: # Should Not be a text file when improved!
                write_str = snid
                write_str += ','.join(map(str, r.parameters)) 
                # We should only keep the the independent components
                # unlike what I am doing here
	        write_str += ','.join(map(str, np.asarray(r.covariance).flatten().tolist()))
                fh.write(write_str)
	except:
	    print('SN {} failed'.format(i))
