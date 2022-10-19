!del Done.txt
set print elements 0
set print repeats 0
set pagination off
target remote localhost:3333
load
break 57
set $j=0
while($j<I_LOOP)
    break gdb_anchor
    continue
    n
    n
    eval "set logging file %i.txt", $j
    set logging on
    set $i=0
        while($i<size_array_res_ania)
            print /d *(res+i)
            set $i=$i+1
        end
    set logging off
    set $j=$j+1
end
break 76
continue
set logging file Done.txt
set logging on
set logging off

continue