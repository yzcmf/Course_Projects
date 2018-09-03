package uiuc.cs463sp16.mp1.test;

import org.junit.runner.JUnitCore;
import org.junit.runner.Result;
import org.junit.runner.notification.Failure;

public class MP1TestRunner
{
    public static void main(String[] args) 
    {
	Result res = JUnitCore.runClasses(MP1Tests.class);
	
	for (Failure fail : res.getFailures()) 
	{
	    System.out.println("Test failed - " + fail.toString());
	}
	
	int runCount = res.getRunCount();
	
	System.out.println("Tests took " + res.getRunTime() / 1000.0 
		+ " seconds. Successful tests: " + (runCount - res.getFailureCount()) + " ouf of " + runCount + "!");
    }
}
