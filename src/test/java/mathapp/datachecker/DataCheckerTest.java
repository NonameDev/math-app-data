package mathapp.datachecker;

import org.junit.Test;

/**
 * Unit test for DataChecker
 */
public class DataCheckerTest  {

    @Test
    public void validateActualData() throws Exception {
        final DataChecker dataChecker = new DataChecker();
        dataChecker.validateData();
    }
}
