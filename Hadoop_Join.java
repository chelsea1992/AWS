
import java.io.IOException;
import org.apache.hadoop.conf.Configuration;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;

import org.apache.hadoop.mapreduce.Job;

import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;

import java.util.StringTokenizer;
import java.util.ArrayList;
import java.util.Iterator;

public class Join {

    public static class AgeFileMapper extends Mapper<Text, Text, Text, Text> {
        private Text outputKey = new Text();
        private Text outputValue = new Text();

        public void map(Text key, Text value, Context context) throws IOException, InterruptedException {
            outputKey = key;
            outputValue.set("a"+","+value.toString());
            context.write(outputKey, outputValue);
        }
    }

    public static class WeightFileMapper extends Mapper<Text, Text, Text, Text> {
        private Text outputKey = new Text();
        private Text outputValue = new Text();

        public void map(Text key, Text value, Context context) throws IOException, InterruptedException {
            outputKey = key;
            outputValue.set("w"+","+value.toString());
            context.write(outputKey, outputValue);
        }
    }

    public static class JoinReducer extends Reducer<Text, Text, Text, Text> {
        private Text outputKey = new Text();
        private Text outputValue = new Text();

        public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
            ArrayList<String> ages = new ArrayList<String>();
            ArrayList<String> weights = new ArrayList<String>();

		    for (Text val : values) {
		     	String[] arr = val.toString().trim().split(",");
    		  	if(arr[0].equals("a")){
    		  	    ages.add(arr[1]);
    		  	} else if(arr[0].equals("w")){
                    weights.add(arr[1]);
    		    }
            }

		    for(String age: ages) {
		    	for(String weight: weights) {
		    	    outputKey = key;
		    	    outputValue.set("("+age+", "+weight+")");
		   	        context.write(outputKey, outputValue);
		    	}
		    }
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();

        if (args.length != 3) {
            System.err.println("Usage: Join <age-in> <weight-in> <out>");
            System.exit(2);
        }


        Job job = Job.getInstance(conf, "join");
        job.setJarByClass(Join.class);

        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(Text.class);

        job.setReducerClass(JoinReducer.class);

        MultipleInputs.addInputPath(job,
                new Path(args[0]),
                KeyValueTextInputFormat.class,
                AgeFileMapper.class);

        MultipleInputs.addInputPath(job,
                new Path(args[1]),
                KeyValueTextInputFormat.class,
                WeightFileMapper.class);

        FileOutputFormat.setOutputPath(job, new Path(args[2]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);

    }
}

