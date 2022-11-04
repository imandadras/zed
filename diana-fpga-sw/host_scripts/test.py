start_r=0
range_r=128

if 511<(start_r%640)<640:
    start_r=(((start_r//640)+1)*640)+(start_r%640)
end_r = start_r + range_r
if 511<(end_r%640)<640:
    end_r=(((end_r//640)+1)*640)+(end_r%640)

print (start_r,end_r)