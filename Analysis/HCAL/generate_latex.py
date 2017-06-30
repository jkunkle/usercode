rbx_start = 2

sub_order = ['HBM', 'HEM', 'HBM', 'HEM','HBP', 'HEP', 'HBP', 'HEP' ]
sub_order_hf = ['HFM', 'HFP']
rbx_list_hf = range( 1, 13 )

rbx_list = range( 1, 19 )

mod_rbx_list = []

for rbx  in rbx_list :
    if rbx >= rbx_start :
        mod_rbx_list.append( rbx )

for rbx in rbx_list :
    if rbx < rbx_start :
        mod_rbx_list.append( rbx )


text = []

text.append( r'\documentclass[12pt]{article}' )
text.append( r'\usepackage{graphicx}' )
text.append( r'\usepackage[letterpaper, margin=0.2in]{geometry}' )
text.append( '' )
text.append( r'\begin{document}' )
text.append( '' )

hist_list = []
det_order_pos = 0
rbx_pair = 0
rbx_pos = 0
rbx_count = 0
pair_idx = 0
while 1 :

    rbx_pos = rbx_pair*2 + pair_idx

    pair_idx += 1
    if pair_idx == 2 :
        pair_idx = 0

    rbx_count += 1
    if rbx_count%4 == 0 :
        rbx_pair += 1



    print rbx_count
    print rbx_pair
    print rbx_pos

        
    if rbx_pos >= len(mod_rbx_list) :
        break

    rbx = mod_rbx_list[rbx_pos]
    print 'rbx = ', rbx

    for det in sub_order[det_order_pos:] :
        # loop around
        det_order_pos += 1
        if det_order_pos >= len(sub_order) :
            det_order_pos = 0

        hist_list.append( '%s%02d' %( det, rbx ) )
        print hist_list[-1]

        if det_order_pos%2 == 0 :
            break


for rbx in rbx_list_hf :
    for det in sub_order_hf :
        hist_list .append( '%s%02d' %( det, rbx ) )

print hist_list

text.append( r'\begin{figure}' )
text.append( r'\centering' )

for idx, rbx in enumerate(hist_list) :

    inc_text  =r'\includegraphics[width=1.0\textwidth]' + '{hists_%s.pdf}' %rbx

    # make a new figure

    if idx%4 == 0 :
        text.append( r'\end{figure}' )
        text.append( '' )
        text.append( r'\clearpage' )
        text.append( '' )
        text.append( r'\begin{figure}' )
        text.append( r'\centering' )
        text.append( inc_text )
        text.append( '' )

    else :
        text.append( inc_text )
        text.append( '' )


text.append( r'\end{figure}' )
text.append( r'\end{document}' )
print text

ofile = open( 'comb.tex', 'w' )

for line in text :
    print line

    ofile.write( line+ '\n' )

ofile.close()
