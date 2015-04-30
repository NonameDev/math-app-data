package mathapp.datachecker;

import org.junit.Test;

/**
 * Created by noname on 4/30/15.
 */
public class DataCheckerTest  {

    @Test
    public void validateActualData() throws Exception {
        final DataChecker dataChecker = new DataChecker();
        dataChecker.validateData();
    }
}
