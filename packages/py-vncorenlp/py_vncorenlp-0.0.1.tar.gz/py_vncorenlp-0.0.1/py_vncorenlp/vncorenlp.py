import jnius_config


class VnCoreNLP:

    def __init__(self, max_heap_size='-Xmx2g', annotators=["wseg", "pos", "ner", "parse"]):
        jnius_config.add_options(max_heap_size)
        jnius_config.set_classpath("./VnCoreNLP-1.1.1.jar")
        from jnius import autoclass
        javaclass_vncorenlp = autoclass('vn.pipeline.VnCoreNLP')
        self.javaclass_String = autoclass('java.lang.String')
        self.annotators = annotators
        if "wseg" not in annotators:
            self.annotators.append("wseg")
        self.model = javaclass_vncorenlp(annotators)

    def annotate_sentence(self, sentence):
        from jnius import autoclass
        javaclass_Annotation = autoclass('vn.pipeline.Annotation')
        str = self.javaclass_String(sentence)
        annotation = javaclass_Annotation(str)
        self.model.annotate(annotation)
        output = annotation.toString().replace("\n\n", "")
        list_words = output.split("\n")
        list_dict_words = []
        for word in list_words:
            dict_word = {}
            word = word.replace("\t\t", "\t")
            list_tags = word.split("\t")
            dict_word["index"] = int(list_tags[0])
            dict_word["wordForm"] = list_tags[1]
            dict_word["posTag"] = list_tags[2]
            dict_word["nerLabel"] = list_tags[3]
            if "parse" in self.annotators:
                dict_word["head"] = int(list_tags[4])
            else:
                dict_word["head"] = list_tags[4]
            dict_word["depLabel"] = list_tags[5]
            list_dict_words.append(dict_word)
        return list_dict_words

    def print_out(self, list_dict_words):
        for word in list_dict_words:
            print(str(word["index"]) + "\t" + word["wordForm"] + "\t" + word["posTag"] + "\t" + word["nerLabel"] + "\t" + str(word["head"]) + "\t" + word["depLabel"])

    def annotate_file(self, input_file, output_file):
        input_str = self.javaclass_String(input_file)
        output_str = self.javaclass_String(output_file)
        self.model.processPipeline(input_str, output_str, self.annotators)

if __name__ == '__main__':
    model = VnCoreNLP(annotators=["parse"])
    output = model.annotate_sentence("Ông Nguyễn Khắc Chúc  đang làm việc tại Đại học Quốc gia Hà Nội.")
    model.print_out(output)
    model.annotate_file(input_file="/home/vinai/Desktop/testvncore/input.txt", output_file="/home/vinai/Desktop/testvncore/output.txt")
