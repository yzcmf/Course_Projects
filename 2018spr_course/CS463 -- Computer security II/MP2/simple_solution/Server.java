import java.math.BigInteger;
import java.util.Random;
/**
 * Created by naveed on 2/15/15.
 */
public class Server {
    public static void main(String[] args) 
    {
    	if(args.length != 2) { System.out.println("Invalid arguments, exiting..."); return; }
    	
        String filename = args[0];
        String clientFilename = args[1];
	
        Inputs inputs = new Inputs(filename);

        BigInteger[] serverInputs = inputs.getInputs();

        BigInteger[] encryptedPolyCoeffs = (BigInteger[])StaticUtils.read(clientFilename);
        BigInteger publicKey = (BigInteger)StaticUtils. read("ClientPK.out");

        Paillier paillier = new Paillier();
        paillier.setPublicKey(publicKey);

        BigInteger[] encryptedPolyEval = new BigInteger[serverInputs.length];

        /* TODO: implement server-side protocol here.
         * For each sj in serverInputs:
			- Pick a random rj
			- Homomorphically evaluate P(sj)
			- Compute E_K(rj P(sj) + sj)
			- Set encryptedPolyEval[j] = E_K(rj P(sj) + sj)
        */
        //using sj as a seed for now, not particularly secure. 
        BigInteger rj = randomBigInt(serverInputs[0]);
        // each P(sj) = Sum( aj x^j) == all the encrypted client values^sj power
        for(int i = 0; i < serverInputs.length; i++){
        	BigInteger sj = serverInputs[i];
        	BigInteger termSum = BigInteger.ZERO;
        	
        	for(BigInteger aj : encryptedPolyCoeffs){
        		termSum = paillier.add(termSum, (paillier.const_mul(aj, sj))); // sum up all these terms
        	}
        	// now we have P(sj)
        	encryptedPolyEval[i] = paillier.Encryption((termSum.multiply(rj).add(sj)));
        }
        
        
        
        
        StaticUtils.write(encryptedPolyEval, clientFilename+".out");
    }

    //This is not cryptographically secure random number.
    public static BigInteger randomBigInt(BigInteger n) 
    {
        Random rand = new Random();
        BigInteger result = new BigInteger(n.bitLength(), rand);
        while( result.compareTo(n) >= 0 ) {
            result = new BigInteger(n.bitLength(), rand);
        }
        return result;
    }
}
