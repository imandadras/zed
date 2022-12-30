import numpy

def check_output(hw_out_fmap,sw_out_fmap_f):
    errors=0
    s_errors=0
    max_error=0
    iterations = hw_out_fmap.shape[1]*hw_out_fmap.shape[2]
    for i in range(hw_out_fmap.shape[1]):
        s = numpy.sum(hw_out_fmap[0][i]-sw_out_fmap_f[0][i])
        if s!=0:
            for j in range(hw_out_fmap.shape[2]):
                ss = numpy.sum(hw_out_fmap[0][i][j]-sw_out_fmap_f[0][i][j])
                if ss!=0:
                    errors+=1
                    if(abs(ss)>hw_out_fmap.shape[3]):
                        s_errors+=1
                        if (abs(ss)/hw_out_fmap.shape[3]>max_error):
                            max_error=abs(ss)/hw_out_fmap.shape[3]
                    print(ss,i,j)
    print("Error %:",errors/iterations*100)
    print("Severe Error %:", s_errors/iterations*100)
    print("Max error:", max_error)