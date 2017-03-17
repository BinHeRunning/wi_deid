import java.io.BufferedReader;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;

import opennlp.tools.chunker.ChunkerME;
import opennlp.tools.chunker.ChunkerModel;
import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSTaggerME;
import opennlp.tools.tokenize.Tokenizer;
import opennlp.tools.tokenize.TokenizerME;
import opennlp.tools.tokenize.TokenizerModel;
import opennlp.tools.sentdetect.SentenceModel;
import opennlp.tools.sentdetect.SentenceDetectorME;

public class ST {
    public static void main(String[] args){
        //args[datapath, modelpath, foldertype]
        try {
            System.out.print("Sentence detector model and Tokenizer model loading...\n");
            //sentencesplit
            InputStream modelIn_sd = new FileInputStream(args[1] + "/en-sent.bin");
            SentenceModel model = new SentenceModel(modelIn_sd);
            SentenceDetectorME sentenceDetector = new SentenceDetectorME(model);

            //tokenizer
            InputStream modelIn_t = new FileInputStream(args[1] + "/en-token.bin");
            TokenizerModel model_t = new TokenizerModel(modelIn_t);
            Tokenizer tokenizer = new TokenizerME(model_t);

            process(sentenceDetector, tokenizer, args[0], args[2]);
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }
        System.out.println(args[2] + " data SentenceDetector and Tokenizer finished!");
    }
        

    private static void process(SentenceDetectorME sentenceDetector, Tokenizer tokenizer, String string1, String string2) throws IOException {
        // TODO Auto-generated method stub
        String text_dir = string1 + "/tempdata/" + string2 + "_text/";

        File sentenceDetector_dir = new File(string1 + "/tempdata/" + string2 + "_sentenceDetector/");
        if(!sentenceDetector_dir.exists()){
            sentenceDetector_dir.mkdir();
        }

        File tokenizer_dir = new File(string1 + "/tempdata/" + string2 + "_tokenizer/"); 
        if(!tokenizer_dir.exists()){
            tokenizer_dir.mkdir();
        }
        
        File userfiles = new File(text_dir);
        for(File file : userfiles.listFiles()){
            //sentenceDetector begin
            String filename = file.getName();
            BufferedReader inputStream_sd = new BufferedReader(new FileReader(file));
            String file_send = sentenceDetector_dir + "/" + filename + ".sd";
            File file_sd = new File(file_send);
            PrintWriter pw_sd = new PrintWriter(file_sd);
            String line_sd = null;
            while((line_sd = inputStream_sd.readLine())!=null)
            {
                if(line_sd.equals(""))
                {
                    continue;
                }
                String sentences[] = sentenceDetector.sentDetect(line_sd);
                int len = sentences.length;
                for(int i=0;i<len;i++)
                {
                    pw_sd.write(sentences[i]+"\n");
                }
            }
            inputStream_sd.close();
            pw_sd.close();
            String filename_sd = file_sd.getName();
            //sentenceDetector end

            //tokenizer begin
            BufferedReader inputStream_t = new BufferedReader(new FileReader(file_sd));
            String file_tok = tokenizer_dir + "/" + filename_sd + ".tok";
            File file_t = new File(file_tok);
            PrintWriter pw_t = new PrintWriter(file_t);
            String line_t = null;
            while((line_t = inputStream_t.readLine())!=null)
            {
                if(line_t.equals(""))
                {
                    continue;
                }
                String tokens[] = tokenizer.tokenize(line_t);
                int len = tokens.length;
                for(int i=0;i<len;i++)
                {
                    pw_t.write(tokens[i]+" ");
                }
                pw_t.write("\n");
            }
            inputStream_t.close();
            pw_t.close();
            //tokenizer end
        }
    }
}
