#/usr/bin/env python
class Unaligned_Sequence_Record():
    """ Class for holding a unaligned sequences """
    def __init__(self, name, headers, sequences):
        self.name = name
        self.headers = headers
        self.sequences = sequences
        self.get_alignment_columns()
        self.index = -1
        self.length = len(self.headers)
    def __iter__(self):
        return self
    def next(self):
        self.index += 1
        if self.index == self.length: 
            self.index = -1
            raise StopIteration
        #return "index =" + str(self.index)
        #return self.iterator[self.index]
        return { 'header' : self.headers[self.index],
                 'sequence' : self.sequences[self.index]}
    def __str__(self):
        output_string = ""
        output_string += "Unaligned_Sequence_Record: {0}\n".format( self.name )
        for i in range(len(self.headers)):
            output_string += ">{0}\n{1}...\n".format( self.headers[i], self.sequences[i][:50] )
        output_string += "{0} sequences in record".format(len(self))
        return output_string
    def __len__(self):
        return self.length
    def get_alignment_columns(self):
        pass
    def write_fasta(self):
        pass
    def write_nexus(self,outfile,sequence_type='protein'):
        maxlen = len(max(self.sequences,key=len))
        lines = [ "{0:<29} {1:-<{2}}".format(x,y,maxlen) for (x,y) in zip(self.headers,self.sequences) ]
        file_header =  "#NEXUS\n\n"
        file_header += "begin data;\n"
        file_header += "    dimensions ntax={0} nchar={1};\n".format(self.length,maxlen)
        file_header += "    format datatype={0} interleave=no gap=-;\n".format(sequence_type)
        file_header += "    matrix\n\n"

        file_footer = "    ;\n\nend;"

        s = file_header + '\n'.join(lines) + file_footer
        open(outfile,'w').write(s)



class Aligned_Sequence_Record(Unaligned_Sequence_Record):
    """ Class for holding a sequence alignment """
    def __str__(self):
        output_string = ""
        output_string += "Aligned_Sequence_Record: {0}\n".format( self.name )
        for i in range(len(self.headers)):
            output_string += ">{0}\n{1}...\n".format( self.headers[i], self.sequences[i][:50] )
        output_string += "{0} sequences in record".format(len(self))
        return output_string
    def get_alignment_columns(self): 
        self.columns = []
        for i in range(len(self.sequences[0])):
            column = ""
            for seq in self.sequences:
                column += seq[i]
            self.columns.append(column) 
        
    
def get_fasta_file(fasta_file, name = "no name"):
    """ FASTA format parser: turns fasta file into Alignment_record object """
    headers = []
    sequences = []
    openfile = open(fasta_file,'r')

    #skip over file until first header is found
    while True:
        line = openfile.readline()
        if not line: return
        if line[0] == ">": break
        #we break the loop here at the start of the first record
    
    headers.append(line[1:].rstrip()) #chuck the first header into our list

    while True:
        line = openfile.readline()
        sequence_so_far = [] #build up sequence a line at a time in this list
        while True:
            if not line: break
            elif not line[0] == ">": 
                sequence_so_far.append(line.rstrip())
                line = openfile.readline()    
            else: break
        sequences.append("".join(sequence_so_far).replace(",",""))
        if not line: break
        headers.append(line[1:].rstrip())
    
    #check all sequences the same length
    first_seq_length = len(sequences[0])
    is_alignment = True
    for seq in sequences:
        if len(seq) != first_seq_length:
            is_alignment = False
            break
        else: continue

    #check same number of headers as sequences
    if len(headers) != len(sequences): print "Error matching all headers and sequences"

    if is_alignment: return Aligned_Sequence_Record(name, headers, sequences)
    else: return Unaligned_Sequence_Record(name, headers, sequences)






