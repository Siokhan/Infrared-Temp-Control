/*
 * ExampleLauncher.java
 * Juzzy 1.10
 * Last updated in August 2013
 * Notes: Multiple outputs are now supported for type-1, interval type-2 and zSlices based general type-2 FLSs.
 * Copyright 2012 Christian Wagner All Rights Reserved.
 */
package radiatorFLC;

import java.io.IOException;

/**
 *
 * @author Christian Wagner
 */
public class ExampleLauncher 
{
    public static void main(String args[]) throws IOException
    {
        String s = (
                "Use the following parameters to launch one of the examples:\n"
                + "(all examples are based on the classic -tipping- example, "
                + "where we have two inputs, food and service quality which "
                + "influence the level of tip we would like to give the waiter.)\n"
                + "type1  --> launches a Type-1 Fuzzy Logic System\n"
                + "NStype1  --> launches a Non Singleton Type-1 Fuzzy Logic System\n"
                + "type1-2outputs  --> launches a Type-1 Fuzzy Logic System with 2 outputs\n"
                + "intervalT2  --> launches a Interval Type-2 Fuzzy Logic System\n"
                + "type1NSintervalT2  --> launches a type-1 Non Singleton Interval Type-2 Fuzzy Logic System\n"
                + "IT2NSintervalT2  --> launches a Interval Type-2 Non Singleton Interval Type-2 Fuzzy Logic System\n"
                + "intervalT2-2outputs  --> launches a Interval Type-2 Fuzzy Logic System with 2 output\n"
                + "zSlicesGT2  --> launches a zSlices based General Type-2 Fuzzy Logic System\n"
                + "type1NSzSlicesGT2  --> launches a zSlices based type-1 Non Singleton General Type-2 Fuzzy Logic System\n"
                + "IT2NSzSlicesGT2  --> launches a zSlices based IT2 Non Singleton General Type-2 Fuzzy Logic System\n"
                + "GT2NSzSlicesGT2  --> launches a zSlices based GT2 Non Singleton General Type-2 Fuzzy Logic System\n"
                + "zSlicesGT2MC  --> launches a zSlices based General Type-2 Fuzzy Logic System in MultiCore Mode\n"
                + "zSlicesGT2MC-2outputs  --> launches a zSlices based General Type-2 Fuzzy Logic System with 2 outputs in MultiCore Mode");
        if(args.length==0)
        System.out.println(s);
        else if(args[0].equals("type1"))
            new thermalRadiatorFLC();          
        else
            System.out.println("Sorry, the parameter provided was not recognized\n\n"+s);
            
    }
            
}
