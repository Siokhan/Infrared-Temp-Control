/*
 * thermalRadiatorFLC.java
 *
 * Created on March 2019
 *
 */
package radiatorFLC;

import generic.Input;
import generic.Output;
import generic.Tuple;
import tools.JMathPlotter;
import type1.sets.T1MF_Gauangle;
import type1.sets.T1MF_Gaussian;
import type1.sets.T1MF_Interface;
import type1.sets.T1MF_Triangular;
import type1.system.T1_Antecedent;
import type1.system.T1_Consequent;
import type1.system.T1_Rule;
import type1.system.T1_Rulebase;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.IOException;

/**
 * A type-1 FLS based on the "Heating level detected from a thermal image"
 * We have one input: heating level and as an output we would
 * like to generate how much the heater power needs to be output, ranging
 * from 0% heating power to 100% power.
 * Code modified from Christian Wagner's Juzzy application.
 * @author Siokhan Kouassi
 */
public class thermalRadiatorFLC 
{
    Input temperature;    //the inputs to the FLS
    Output radiatorPower;   //the output of the FLS
    T1_Rulebase rulebase;   //the rulebase captures the entire FLS
    
    public thermalRadiatorFLC() throws IOException
    {
        //Define the inputs
        temperature = new Input("Temperature Feeling", new Tuple(0,10));      //heating level detected from thermal image
        radiatorPower = new Output("Radiator Power Output", new Tuple(0,100)); //a percentage for the radiatorPower

        //Set up the membership functions (MFs) for each input and output
        T1MF_Gauangle coldTempMF = new T1MF_Gauangle("MF for cold temperature",0.0, 0.0, 6.0);
        T1MF_Gauangle normalTempMF = new T1MF_Gauangle("MF for normal temperature",2.5, 5.0, 7.5);
        T1MF_Gauangle hotTempMF = new T1MF_Gauangle("MF for hot temperature",4.0, 10.0, 10.0);

        T1MF_Gaussian decreasePowerMF = new T1MF_Gaussian("Low radiatorPower", 0.0, 30.0);
        T1MF_Gaussian steadyPowerMF = new T1MF_Gaussian("Medium radiatorPower", 50.0, 6.0);
        T1MF_Gaussian increasePowerMF = new T1MF_Gaussian("High radiatorPower", 100.0, 30.0);

        //Set up the antecedents and consequents - note how the inputs are associated...
        T1_Antecedent coldTemp = new T1_Antecedent("ColdTemp",coldTempMF, temperature);
        T1_Antecedent normalTemp = new T1_Antecedent("NormalTemp",normalTempMF, temperature);
        T1_Antecedent hotTemp = new T1_Antecedent("HotTemp",hotTempMF, temperature);
        
        
        T1_Consequent decreaseTemp = new T1_Consequent("DecreaseTemp", decreasePowerMF, radiatorPower);
        T1_Consequent steadyTemp = new T1_Consequent("SteadyTemp", steadyPowerMF, radiatorPower);
        T1_Consequent increaseTemp = new T1_Consequent("IncreaseTemp", increasePowerMF, radiatorPower);

        //Set up the rulebase and add rules
        rulebase = new T1_Rulebase(3);
        rulebase.addRule(new T1_Rule(new T1_Antecedent[]{coldTemp}, increaseTemp));
        rulebase.addRule(new T1_Rule(new T1_Antecedent[]{normalTemp}, steadyTemp));
        rulebase.addRule(new T1_Rule(new T1_Antecedent[]{hotTemp}, decreaseTemp));
         
        //just an example of setting the discretisation level of an output - the usual level is 100
        radiatorPower.setDiscretisationLevel(50);        
        
        //get some outputs using readInput function
        //string is then converted to double in order to appropriately
        //calculate radiator power output
        String [] heatLvlTxt = readInput("/Users/siokhankouassi/Desktop/Dissertation-2/fuzzyLogic/Juzzy/Project/Juzzy_V2_Source/src/radiatorFLC/FLCinput.txt");
        double finalInput = Double.parseDouble(heatLvlTxt[0]);
        System.out.println(finalInput);
        getTemp(finalInput);
        
        //plot some sets, discretizing each input into 100 steps.
        plotMFs("Heating Level Membership Functions", new T1MF_Interface[]{coldTempMF, normalTempMF, hotTempMF}, temperature.getDomain(), 100);
        plotMFs("Radiator Power Output Membership Functions", new T1MF_Interface[]{decreasePowerMF, steadyPowerMF, increasePowerMF}, radiatorPower.getDomain(), 100);
       
        //print out the rules
        System.out.println("\n"+rulebase);        
    }
    
    /**
     * Basic method that prints the output for a given set of inputs.
     * @param temperatureQuality
     */
    private void getTemp(double temperatureQuality)
    {
        //first, set the inputs
        temperature.setInput(temperatureQuality);
        //now execute the FLS and print output
        System.out.println("The temperature was: "+temperature.getInput());
        System.out.println("Using height defuzzification, the FLS recommends a radiatorPower of"
                + "radiatorPower of: "+rulebase.evaluate(0).get(radiatorPower)); 
        System.out.println("Using centroid defuzzification, the FLS recommends a radiatorPower of"
                + "radiatorPower of: "+rulebase.evaluate(1).get(radiatorPower));     
    }
    
    private void plotMFs(String name, T1MF_Interface[] sets, Tuple xAxisRange, int discretizationLevel)
    {
        JMathPlotter plotter = new JMathPlotter(17,17,15);
        for (int i=0;i<sets.length;i++)
        {
            plotter.plotMF(sets[i].getName(), sets[i], discretizationLevel, xAxisRange, new Tuple(0.0,1.0), false);
        }
        plotter.show(name);
    }
    
    //read txt file that contains FLC input number generated by thermal
    //image processing, input as a string into array
    private String[] readInput(String file) throws IOException
    {
        try
        {
            FileReader fr = new FileReader(file);
            BufferedReader textReader = new BufferedReader(fr);
            
            int numOfLines = 1;
            String[] textData = new String[numOfLines];
            
            for(int i = 0; i < numOfLines; i++) 
            {
                textData[i] = textReader.readLine();
            }
            textReader.close();
            return textData;
        }
        catch(FileNotFoundException e)
        {
            System.out.println("file not found");
        }
        return null;
    }
    
    public static void main (String args[]) throws IOException
    {
        new thermalRadiatorFLC();
    }
}
