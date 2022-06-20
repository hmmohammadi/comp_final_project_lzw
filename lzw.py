from codecs import utf_16_le_encode, utf_8_encode
import string
import sys
from struct import pack

class Compression:
    def __init__(self, data, input_file, length=8) -> None:
        ## default dict size extended ascii character
        self.dict_size = 256
        ## Define max table size
        self.MAX_TABLE_SIZE = 2 ** length
        ## Craate a table with extended ascii table
        self.table =[chr(i) for i in range(0, self.dict_size)]
        self.compressed = []
        # sikstirilmis verinin unicode karsiligi
        self.uni_compressed = ""
        # girdi datasi
        self.data = data
        self.file_name = input_file.split(".")[0] + ".lzw"
        self.out_file = open(self.file_name, "wb")

    def compress_lzw(self):
        # import pdb; pdb.set_trace()
        tmp_str = ""
        for letter in self.data:
            current_str = tmp_str + letter
            
            if current_str in self.table: # eger tmp_str ve symbol sozluk icinde varsa tmp_str'i guncelle
                tmp_str = current_str

            else: # yoksa datayi compressed'e ekle
                # bir onceki string'in index'ini sikistirilmis veriyi tutan diziye ekle
                self.compressed.append(self.table.index(tmp_str))

                if (len(self.table) < self.MAX_TABLE_SIZE): # MAX_DIC_SIZE'a ulasilmadiysa 
                    self.table.append(tmp_str + letter)
                # tmp_str onceki data'yi harfi tutsun
                tmp_str = letter
        # son Guncellenmis tmp_str
        self.compressed.append(self.table.index(tmp_str))

        # print(self.compressed)
        ## get the unicodes of integer results of compressed data
        for idx in self.compressed:
            # print(idx, ' ', chr(idx))
            self.uni_compressed += chr(idx)
        
        print(self.uni_compressed)
 
    def save(self):
        # macOs littile endian oldugu icin en fazla tablo boyutu 16^2 bit olarak kabul et
        print(len(self.uni_compressed.encode("UTF-16LE")))
        self.out_file.write(self.uni_compressed.encode("UTF-16LE"))
        self.out_file.close()


class Decompression:

    def __init__(self, data, input_file, length=8) -> None:
        self.data = data
        self.MAX_TABLE_SIZE = 2 ** length
        self.dict_size = 256
        self.table =[chr(i) for i in range(0, self.dict_size)]
        self.decompressed = []
        self.file_name = open(input_file.split(".")[0]+"_decoded.txt", "w")
        # pass

    def decompress_lzw(self):

        tmp_str = ""
        tmp_str = self.table[ord(self.data[0])]
        self.decompressed.append(self.table[ord(tmp_str)])
        for c in range(1,len(self.data)):
            if ord(self.data[c]) >= len(self.table): ## Eger integer degeri tablonun uzunlugunu gecerse(tablo olustuktan sonra tabloya eklenmis yeni pattern ise)
                current = tmp_str + tmp_str[0] ## bir onceki ile bir sonrakini birlestir
            else:
                current = self.table[ord(self.data[c])]
            self.decompressed.append(current)
            if len(self.table) < self.MAX_TABLE_SIZE:
                self.table.append(tmp_str + current[0])
            tmp_str = current
        

            
    
    def save(self):
        # file_name = open("decompressed_dataa" + ".txt", "wb")
        
        self.file_name.write(''.join(self.decompressed))
        
        self.file_name.close()

def main():

    intput_file, bit_length, is_comp = sys.argv[1:]
    if int(is_comp) == 0:

        print("compressing")
        file = open(intput_file)
        data = file.read()

        print(len(data))

        comp = Compression(data=data, input_file=intput_file ,length=int(bit_length))
        # print(comp.table)
        comp.compress_lzw()
        comp.save()

        file.close()

    elif int(is_comp) == 1:

        print("Decompressing")
        # dosya nasil kaydedildiysa o sekilde oku.
        file = open(intput_file, 'r', encoding="UTF-16LE")
        data = file.read()

        decomp = Decompression(data=data, input_file=intput_file, length=int(bit_length))
        decomp.decompress_lzw()
        decomp.save()

        file.close()
    else:
        print("Wrong input !!!!!")
    
    # pass




if __name__=="__main__":
    main()

                


