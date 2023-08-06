#!/usr/bin/env python
__version__='0.1.4'
last_update='2022-06-20'
author='Damien Marsic, damien.marsic@aliyun.com'
license='GNU General Public v3 (GPLv3)'

import dmbiolib as dbl
import argparse,glob,sys
from Bio.Seq import Seq
from collections import defaultdict
from matplotlib import pyplot as plt

def main():
    parser=argparse.ArgumentParser(description="Analysis of insertion sites in viral or microbial genomes using either LAM-PCR or whole genome sequencing. For full documentation, visit: https://insertmap.readthedocs.io")
    parser.add_argument('-v','--version',nargs=0,action=override(version),help="Display version")
    subparser=parser.add_subparsers(dest='command',required=True)
    parser_a=subparser.add_parser('lampcr',help="Detect insertion sites using LAM-PCR derived amplicon libraries")
    parser_a.add_argument('-c','--configuration_file',default='insertmap_lampcr.conf',type=str,help="Configuration file for the insertmap lampcr program (default: insertmap_lampcr.conf), will be created if absent")
    parser_a.add_argument('-n','--new',default=False,action='store_true',help="Create new configuration file and rename existing one")
    parser_b=subparser.add_parser('wgs',help="Detect insertion sites using WGS libraries")
    parser_b.add_argument('-c','--configuration_file',default='insertmap_wgs.conf',type=str,help="Configuration file for the insertmap lampcr program (default: insertmap_wgs.conf), will be created if absent")
    parser_b.add_argument('-n','--new',default=False,action='store_true',help="Create new configuration file and rename existing one")
    parser_c=subparser.add_parser('analyze',help="Analyze data")
    parser_c.add_argument('-c','--configuration_file',default='lampcr_analyze.conf',type=str,help="Configuration file for the lampcr analyze program (default: lampcr_analyze.conf), will be created if absent")
    parser_c.add_argument('-n','--new',default=False,action='store_true',help="Create new default configuration file and rename existing one")
    args=parser.parse_args()
    if args.command in 'lampcr,wgs':
        rmap(args)
    if args.command=='analyze':
        analyze(args)

def rmap(args):
    rname='insertmap_'+args.command+'-report.txt'
    dbl.rename(rname)
    r=open(rname,'w')
    fname=args.configuration_file
    if args.new:
        dbl.rename(fname)
    if args.new or not dbl.check_file(fname,False):
        mapconf(fname,args)
        return
    print('\n  Checking configuration... ',end='')
    f=open(fname,'r')
    read=''
    rfiles=[]
    ins={}
    linker={}
    host=''
    insseq={}
    probe=10
    fail=''
    for line in f:
        ln=line.strip()
        if ln[:1]=='#':
            read=''
        if ln[:12]=='# READ FILES':
            read='rfiles'
        if ln[:13]=='# INSERT SITE':
            read='insert'
        if ln[:13]=='# LINKER SITE':
            read='linker'
        if ln[:13]=='# HOST GENOME':
            read='host'
        if ln[:7]=='# PROBE':
            read='probe'
        if ln[:11]=='# INSERTION':
            read='insseq'
        if ln[:3]=='===' or ln[:2]=='# ' or ln[:13]=='Instructions:' or not ln:
            continue
        if ln and read=='rfiles':
            x=ln.split()
            fail+=dbl.check_read_file(x[-1])
            if len(x)>3:
                fail+='\n  Too many items per line under READ FILES! Each line must contain a prefix followed by 1 or 2 (if paired-ends) read files, separated by space or tab!'
            if len(x)==3:
                fail+=dbl.check_read_file(x[1])
            if len(x)==1 or (len(x)==2 and glob.glob(x[0])):
                if '-' in x[0]:
                    z=x[0][:x[0].find('-')]
                else:
                    z=x[0][:x[0].find('_')]
                x.insert(0,z)
            if x[0] in [k[0] for k in rfiles]:
                fail+='\n  Duplicate prefix '+x[0]+' found under READ FILES! Each line must contain a different prefix!'
            else:
                rfiles.append(x)
        for n in (('insert',ins),('linker',linker)):
            if ln and read==n[0]:
                x=ln.split()
                if len(x)!=2:
                    fail+='\n  Each line under '+n[0].upper()+' SITE COMMON SEQUENCE must contain a name and a nucleotide sequence, separated by a space or tab!'
                else:
                    t,req=dbl.check_seq(x[1],'atgcryswkmbdhvn','atgc')
                    if not t or not req:
                        fail+='\n  Invalid characters were found under '+n[0].upper()+' SITE COMMON SEQUENCE!'
                    elif x[0] in ins or x[0] in linker:
                        fail+='\n  Duplicate '+n[0]+' name '+x[0]+' found! All insert and linker sequences must have different names!'
                    else:
                        c=x[1].lower()
                        a=len(c)
                        b=0
                        for i in range(len(c)):
                            if c[i] not in 'atgc':
                                a=i
                                break
                        for i in reversed(range(len(c))):
                            if c[i] not in 'atgc':
                                b=i+1
                                break
                        z=c.count('n')
                        y=[c[b:],b,z]  # constant region of sequence (after non-atgc region if present), index, number of N
                        if y in ins.values() or y in linker.values():
                            fail+='\n  Duplicate sequence found: '+x[0]+' !'
                        else:
                            n[1][x[0]]=y
        if ln and read=='host':
            x,y=dbl.getfasta(ln,'atgcryswkmbdhvn','atgc',False)
            if y:
                fail+=y
            else:
                host=list(x.values())[0]
                hname=list(x.keys())[0]
        if ln and read=='probe':
            if not ln.isdigit() or int(ln)<10 or int(ln)>50:
                fail+='\n  Probe length must be an integer between 10 and 50'
            else:
                probe=int(ln)
        if ln and read=='insseq':
            x,y=dbl.getfasta(ln,'atgcryswkmbdhvn','atgc',True)
            if y:
                fail+=y
            else:
                insseq.update(x)
    f.close()
    insprobe={}
    if insseq:
        insrc={}
        for n in insseq:
            insrc[n]=str(Seq(insseq[n]).reverse_complement())
        q,y=dbl.shortest_probe(list(insseq.values())+list(insrc.values()),probe,host,'insert')
        fail+=y
        if not y:
            for n in insseq:
                insprobe[n]=(insrc[n][-q:],insseq[n][-q:],insseq[n][:q],insrc[n][:q])  # left 3', right 3', left 5', right 5'
    if ins:
        q,y=dbl.shortest_probe([k[0] for k in list(ins.values())+list(linker.values())],probe,host,'insert or linker')
        fail+=y
        if not y:
            for n in ins:
                insprobe[n]=(ins[n][0][-q:],ins[n][1]+len(ins[n][0])-q)  # probe sequence, index
            for n in linker:
                insprobe[n]=(linker[n][0][-q:],linker[n][1]+len(linker[n][0])-q)
    if not rfiles:
        fail+='\n  Read files are missing!'
    if args.command=='lampcr':
        if not ins:
            fail+='\n  Insert site common sequence is missing!'
        if rfiles and len(rfiles[0])==3 and not linker:
            fail+='\n  Linker site common sequence is missing!'
        if rfiles and len(rfiles[0])==2 and linker:
            fail+='\n  R2 read file is missing!'
    elif not insseq:
        fail+='\n  Insert sequence is missing!'
    if not host:
        fail+='\n  Host genome sequence is missing!'
    if fail:
        print('\n'+fail+'\n')
        sys.exit()
    fail=''
    r.write('\n  Host genome: '+hname)
    if ins:
        r.write('\n\n  Insert site common sequence(s):\n  '+'\n  '.join([k+'\t'+ins[k][0] for k in ins]))
    if linker:
        r.write('\n\n  Linker site common sequence(s):\n  '+'\n  '.join([k+'\t'+linker[k][0] for k in linker]))
    if insseq:
        r.write('\n\n  Insertion sequence(s): '+', '.join([k for k in insseq]))
    r.write('\n\n  Probe size: '+str(probe)+'\n\n')
    print('OK\n\n  Checking read files...    ',end='')
    for j in range(len(rfiles)):
        R1=rfiles[j][1]
        nr1,fail=dbl.readcount(R1,fail)
        rfiles[j].append(nr1)
        R2=''
        if len(rfiles[j])==4:
            R2=rfiles[j][2]
            nr2,fail=dbl.readcount(R2,fail)
            rfiles[j].append(nr2)
            if args.command=='lampcr' and nr1>1 and nr2>1 and nr1!=nr2:
                fail+='\n  Paired files '+R1+' and '+R2+' have different numbers of reads! You must use raw read files!'
        if args.command=='lampcr' and R2:
            f1,y1,c1=dbl.initreadfile(R1)
            f2,y2,c2=dbl.initreadfile(R2)
            z=[False,False,False,False]   # insert in R1, linker in R1, insert in R2, linker in R2
            for i in range(100):
                l1,f1,c1,n1=dbl.getread(f1,y1,c1)
                l2,f2,c2,n2=dbl.getread(f2,y2,c2)
                if not l1 or not l2:
                    break
                x=dbl.check_sync(n1,n2)
                fail+=x
                if x:
                    break
                x,_=probe_get(l1,insprobe)
                if x in ins:
                    z[0]=True
                elif x:
                    z[1]=True
                x,_=probe_get(l2,insprobe)
                if x in ins:
                    z[2]=True
                elif x:
                    z[3]=True
            f1.close()
            f2.close()
            if z==[True,False,False,True]:
                x=['R1','R2']
            elif z==[False,True,True,False]:
                x=['R2','R1']
            else:
                x=['mixed','mixed']
            rfiles[j].extend(x)
    if fail:
        dbl.pr2(r,'Problems found!\n'+fail+'\n')
    else:
        print('OK\n')
    if (args.command=='lampcr' and R2) or not R2:
        x='  Read file prefix         Number of read'
        if R2:
            x+=' pairs      Insert reads      Linker reads'
        else:
            x+='s'
        dbl.pr2(r,x)
        for n in rfiles:
            x='  '+n[0].ljust(25)
            if R2:
                x+=f'{n[3]:,}'.rjust(20)+n[-2].center(24)+n[-1].center(12)
            if not R2:
                x+=f'{n[2]:,}'.rjust(15)
            if not R2 or (R2 and n[3]==n[4]):
                dbl.pr2(r,x)
    else:
        dbl.pr2(r,'  Read file prefix         Read file                     Number of reads')
        for n in rfiles:
            dbl.pr2(r,'  '+n[0].ljust(25)+n[1].ljust(30)+f'{n[3]:,}'.rjust(15)+'\n  '+n[0].ljust(25)+n[2].ljust(30)+f'{n[4]:,}'.rjust(15))
    dbl.pr2(r,'')
    if fail:
        r.close()
        sys.exit()
    UMI={}
    t=' nt UMI detected in '
    for n in ins:
        if not R2:
            if ins[n][2]>7:
                UMI[n]=True
                dbl.pr2(r,'  '+str(ins[n][2])+t+n+'\n')
            else:
                UMI[n]=False
        for m in linker:
            if linker[m][2]>7:
                UMI[(n,m)]=(False,True)
                x=m
                y=linker[m][2]
            elif ins[n][2]>7:
                UMI[(n,m)]=(True,False)
                x=n
                y=ins[n][2]
            elif ins[n][2]+linker[m][2]>7:
                UMI[(n,m)]=(True,True)
                x=n+'-'+m
                y=ins[n][2]+linker[m][2]
            else:
                UMI[(n,m)]=(False,False)
                x=''
            if x:
                dbl.pr2(r,'  '+str(y)+t+x+'\n')
    for rfile in rfiles:
        pre=rfile[0]
        R1=rfile[1]
        f1,y1,c1=dbl.initreadfile(R1)
        R2=''
        if len(rfile)>4:
            R2=rfile[2]
            f2,y2,c2=dbl.initreadfile(R2)
        imap={}
        cnt={}
        for n in insseq:
            imap[n]=defaultdict(int)
            cnt[n]=[0,0]  # insert identified, insertion site identified
        for n in ins:
            for m in linker:
                if True in UMI[(n,m)]:
                    imap[(n,m)]=defaultdict(lambda: defaultdict(int))
                else:
                    imap[(n,m)]=defaultdict(int)
                cnt[(n,m)]=[0,0,0,0,0]  # insert identified, insertion site identified, linker identified, shear site identified, PCR replicates discarded
            if not R2:
                if UMI[n]==True:
                    imap[n]=defaultdict(lambda: defaultdict(int))
                else:
                    imap[n]=defaultdict(int)
                cnt[n]=[0,0,0]  # insert identified, insertion site identified, PCR replicates discarded
        X=[(R1,f1,y1,c1)]
        if R2:
            X.append((R2,f2,y2,c2))
        for j in (0,1):
            f,y,c=X[j][1],X[j][2],X[j][3]
            if not R2 or (args.command=='lampcr' and j):
                break
            nr=rfile[2+j]
            if R2:
                nr=rfile[3+j]
            x=pre
            if insseq:
                x=X[j][0]
            t='Processing reads from '+x+'...'
            show=dbl.progress_start(nr,t)
            while True:
                if args.command=='wgs':
                    l,f,c,_=dbl.getread(f,y,c)
                    if not l:
                        break
                    dbl.progress_check(c,show,t)
                    for n in insseq:
                        for m in insprobe[n]:
                            a=l.find(m)
                            if a==-1:
                                continue
                            cnt[n][0]+=1
                            if m in insprobe[n][:2]:
                                dir=1
                                A=l[a+len(m):]
                            else:
                                dir=0
                                A=l[:a]
                            x=seq_locate(A,dir,host,probe)
                            if x==-1:
                                continue
                            cnt[n][1]+=1
                            imap[n][x]+=1    
                elif args.command=='lampcr':
                    l1,f1,c1,n1=dbl.getread(f1,y1,c1)
                    if R2:
                        l2,f2,c2,n2=dbl.getread(f2,y2,c2)
                    if not l1 or (R2 and not l2):
                        break
                    if R2:
                        x=dbl.check_sync(n1,n2)
                        if x:
                            dbl.pr2(r,x)
                            r.close()
                            sys.exit()
                    dbl.progress_check(c,show,t)
                    if R2 and rfile[-1]=='R1':
                        l1,l2=l2,l1
                    n,a=probe_get(l1,insprobe)   # n: name of ins or linker, a: index of seq to be searched in host
                    if not n:
                        continue
                    if R2:
                        if rfile[-1]=='mixed' and n in linker:
                            m,b,l2,l1=n,a,l1,l2
                            n,a=probe_get(l1,{i:insprobe[i] for i in ins})
                        else:
                            m,b=probe_get(l2,{i:insprobe[i] for i in linker})
                        if n:
                            cnt[(n,m)][0]+=1
                        if m:
                            cnt[(n,m)][2]+=1
                        if not n or not m:
                            continue
                        x=seq_locate(l1[a:],1,host,probe)
                        if x==-1:
                            continue
                        cnt[(n,m)][1]+=1
                        y=seq_locate(l2[b:],1,host,probe)
                        if y:
                            cnt[(n,m)][3]+=1
                        if True in UMI[(n,m)]:
                            u=''
                            if UMI[(n,m)][0]==True:
                                u+=l1[:ins[n][1]]
                            if UMI[(n,m)][1]==True:
                                u+=l2[:linker[n][1]]
                            imap[n][(x,y)][u]+=1
                            if imap[n][(x,y)][u]>1:
                                cnt[(n,m)][-1]+=1
                        else:
                            imap[n][(x,y)]+=1
                    else:
                        cnt[n][0]+=1
                        x=seq_locate(l1[a:],1,host,probe)
                        if x==-1:
                            continue
                        cnt[n][1]+=1
                        if UMI[n]==True:
                            imap[n][x][l1[:ins[n][1]]]+=1
                            if imap[n][x][l1[:ins[n][1]]]>1:
                                cnt[n][-1]+=1
                        else:
                            imap[n][x]+=1
            dbl.progress_end()
        f1.close()
        if R2:
            f2.close()
        x='s'
        if args.command=='lampcr' and R2:
            x=' pairs'
            c=c1
        dbl.pr2(r,('  Read'+x+' processed:').ljust(48)+f'{c:,}'.rjust(15))
        for n in insseq:
            dbl.pr2(r,'\n  Insert: '+n)
            dbl.pr2(r,'  Number of insert ends found:'.ljust(45)+f'{cnt[n][0]:,}'.rjust(15))
            dbl.pr2(r,'  Number of insertion site identifications:'.ljust(45)+f'{cnt[n][1]:,}'.rjust(15))
            dbl.pr2(r,'  Number of different insertion sites:'.ljust(45)+f'{len(imap[n]):,}'.rjust(15))
            x=pre+'-'+n+'_imap.csv'
            f=open(x,'w')
            for m in sorted(imap[n]):
                f.write(str(m)+','+str(imap[n][m])+'\n')
            f.write('\n')
            f.close()
            dbl.pr2(r,'\n  Insertion map was saved into file: '+x+'\n')
        for c in cnt:
            x=''
            y=c
            if R2:
                x='-linker pair'
                y=str(c)[1:-1].replace("'",'').replace(', ','-')
            dbl.pr2(r,'\n  Insert'+x+': '+y)
            dbl.pr2(r,'  Number of insert identifications:'.ljust(48)+f'{cnt[c][0]:,}'.rjust(15))
            dbl.pr2(r,'  Number of insertion site identifications:'.ljust(48)+f'{cnt[c][1]:,}'.rjust(15))
            dbl.pr2(r,'  Number of different insertion sites:'.ljust(48)+f'{len(imap[c]):,}'.rjust(15))    ####use Counter() ?
            if R2:
                dbl.pr2(r,'  Number of linker identifications:'.ljust(48)+f'{cnt[c][2]:,}'.rjust(15))
                dbl.pr2(r,'  Number of shear site identifications:'.ljust(48)+f'{cnt[c][3]:,}'.rjust(15))
                dbl.pr2(r,'  Number of different shear sites:'.ljust(48)+f'{len(imap[c]):,}'.rjust(15))        ####use Counter() ?
            if UMI[c]==True or (R2 and True in UMI[c]):
                dbl.pr2(r,'  Number of insert-linker-UMI replicates found:'.ljust(48)+f'{cnt[c][-1]:,}'.rjust(15))



        ###  save lampcr data into csv files !!!

#  Make seq_locate faster: start with sort seq (probe ?) and increase size until single match

# CASE STRETCH OF N IN INSSEQ !!!!!


    r.close()
    print('  Report was saved into file: '+rname+'\n')

def analyze(args):
    pass

    ####################





def mapconf(fname,args):
    f=open(fname,'w')
    f.write('=== INSERTMAP '+args.command.upper()+' CONFIGURATION FILE ===\n\n')
    f.write('# READ FILES\nInstructions: list prefix (to be used in output file names) and read file names, one pair of files (paired-end data) / one file (single end data) per line, separated by space or tab\n\n')
    y=dbl.find_read_files()
    f.write('\n'.join(y)+'\n\n')
    f.write('# HOST GENOME\nInstructions: write name of the file containing the host genome sequence (FASTA format only).\n\n')
    x=glob.glob('*.f*a')
    y=''
    if len(x)==1:
        y=x[0]
    elif len(x)>1:
        y=[dbl.fsize(k) for k in x]
        y=x[y.index(max(y))]
    if y:
        f.write(y+'\n\n')
    if args.command=='lampcr':
        f.write('# INSERT SITE COMMON SEQUENCE(S)\nInstructions: write the name and entire common sequence of each read preceding the host sequence (primer + sequence downstream), including any diversity sequence or tag (as NNNN...), one per line, name and sequence separated by space or tab.\n\n\n\n')
        f.write('# LINKER SITE COMMON SEQUENCE(S) (paired-end only)\nInstructions: write the name and entire common sequence of each read preceding the host sequence (primer + sequence downstream), including any diversity sequence or tag (as NNNN...), one per line, name and sequence separated by space or tab.\n\n')
    else:
        f.write('# INSERTION SEQUENCE(S)\nInstructions: write name(s) of file(s) containing the insert sequence(s), either a single multifasta file or multiple fasta files, one file name per line. Unknown or variable internal regions can be represented by stretches of N.\n\n')
        if len(x)>1:
            x.remove(y)
            f.write('\n'.join(x)+'\n\n')
    f.write('# PROBE LENGTH\nInstructions: minimum length in nt of sequences used as probes to identify insertions (integer between 10 and 50, larger is faster but less accurate).\n\n10\n\n')
    f.write('=== END OF CONFIGURATION FILE ===')
    f.close()
    print('\n  Edit the file '+fname+' before running insertmap '+args.command+' again !\n\n')

def override(func):
    class OverrideAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            func()
            parser.exit()
    return OverrideAction

def version():
    print('\n  Project: '+sys.argv[0][max(sys.argv[0].rfind('\\'),sys.argv[0].rfind('/'))+1:-3]+'\n  Version: '+__version__+'\n  Latest update: '+last_update+'\n  Author: '+author+'\n  License: '+license+'\n')

def probe_get(read,probes):
    for i in (0,-1,1):
        for n in probes:
            if read[probes[n][1]+i:].startswith(probes[n][0]):
                break
        else:
            continue
        break
    else:
        return '',-1
    return n,probes[n][1]+len(probes[n][0])+i

def seq_locate(A,dir,host,probe):
    B=str(Seq(A).reverse_complement())
    x=-1
    while True:
        d=(host+host[:len(A)-1]).count(A)+(host+host[:len(B)-1]).count(B)
        if d>1:
            break
        if d==1:
            x=(host+host[:len(A)-1]).find(A)
            if x==-1:
                x=(host+host[:len(B)-1]).find(B)
            if not dir:
                x+=len(A)
            break
        if len(A)==probe+1:
            break
        if dir:
            A=A[:-1]
            B=B[1:]
        else:
            A=A[1:]
            B=B[:-1]
    return x

if __name__ == '__main__':
    main()

