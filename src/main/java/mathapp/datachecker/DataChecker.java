package mathapp.datachecker;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.Assert;

import java.io.File;
import java.util.Scanner;

import static mathapp.datachecker.Constants.*;

/**
 * Class responsible for validating the data
 */
public class DataChecker {

    /**
     * Path to the directory containing the data
     */
    private String dataDirPath;

    /**
     * Constructor. Defaults the data directory to the directory with the real data
     */
    public DataChecker() {
        this(REAL_DATA_PATH);
    }

    /**
     * Constructor. Sets the data directory path to the given value
     *
     * @param dataDirPath String with the path to the directory containing the data
     */
    public DataChecker(final String dataDirPath) {
        this.dataDirPath = dataDirPath;
    }

    /**
     * Parses the data files in order to ensure their validity
     *
     * @throws Exception If there are any discrepancies in the data
     */
    public void validateData() throws Exception {
        this.checkDataDir(this.dataDirPath);
        final File eqnDataFile = new File(this.dataDirPath + EQN_DATA_FILE_NAME);
        final File versionFile = new File(this.dataDirPath + VERSION_FILE_NAME);
        this.checkFilesExist(eqnDataFile, versionFile);
        final String eqnDataString = this.getFileAsString(eqnDataFile);
        final String versionString = this.getFileAsString(versionFile);
        this.validateVersionFile(versionString);
        this.validateEquationData(eqnDataString);
    }

    /**
     * Checks that the data directory exists
     *
     * @param dataDirPath String with the path to the directory containing
     *                    the data
     */
    private void checkDataDir(final String dataDirPath) {
        final File dataDir = new File(dataDirPath);
        Assert.assertTrue("Data directory does not exist", dataDir.isDirectory());
    }

    /**
     * Checks that both the equation data and the version file exist
     *
     * @param eqnDataFile File that contains the equation data
     * @param versionFile File that contains the version of the current data
     */
    private void checkFilesExist(final File eqnDataFile, final File versionFile) {
        Assert.assertTrue("Equation data file does not exit", eqnDataFile.isFile());
        Assert.assertTrue("Version file does not exit", versionFile.isFile());
    }

    /**
     * Checks that the version file is correct
     *
     * @param content String containing the contents of the version fiel
     */
    private void validateVersionFile(final String content) {
        final JSONObject baseJsonObject = new JSONObject(content);
        Assert.assertTrue("Version data does not contain version", baseJsonObject.has(VERSION_KEY));
        final int versionNum = baseJsonObject.optInt(VERSION_KEY, -1);
        Assert.assertTrue("Version is not an int", versionNum != -1);
    }

    /**
     * Checks that the equation data file is valid
     *
     * @param content String containing the contents of the equation data file
     */
    private void validateEquationData(final String content) {
        final JSONObject baseJsonObject = new JSONObject(content);
        Assert.assertTrue("Equation data does not contain equations", baseJsonObject.has(EQUATIONS_KEY));
        final JSONArray eqnsArray = baseJsonObject.optJSONArray(EQUATIONS_KEY);
        Assert.assertNotNull("Equarions is not an array", eqnsArray);
        for (int i = 0; i < eqnsArray.length(); i++) {
            this.checkEquationJsonObject(eqnsArray.optJSONObject(i));
        }
    }

    /**
     * Cheks that JSON object for the equation data
     *
     * @param obj JSONObject for the equation data
     */
    private void checkEquationJsonObject(final JSONObject obj) {
        Assert.assertNotNull("Equation is not a JSONObject", obj);
        Assert.assertTrue("Equation does not contain name", obj.has(NAME_KEY));
        Assert.assertTrue("Equation does not contain keywords", obj.has(KEYWORDS_KEY));
        Assert.assertTrue("Equation does not contain variables", obj.has(VARIABLES_KEY));
        this.checkName(obj);
        this.checkKeywords(obj);
        this.checkVariables(obj);
    }

    /**
     * Checks the content of the name in the equations JSONObject
     * @param obj JSONObject for the equation data
     */
    private void checkName(final JSONObject obj) {
        final String name = obj.optString(NAME_KEY);
        Assert.assertNotNull("Name is not a String", name);
    }

    /**
     * Checks the contents of the keywords in the equations JSONObject
     *
     * @param obj JSONObject for the equation data
     */
    private void checkKeywords(final JSONObject obj) {
        final JSONArray keywords = obj.optJSONArray(KEYWORDS_KEY);
        Assert.assertNotNull("Keywords is not an array", keywords);
        for (int i = 0; i < keywords.length(); i++) {
            final String keyword = keywords.optString(i);
            Assert.assertNotNull("Keywords is not a String", keyword);
        }
    }

    /**
     * Checks the contents of the keywords in the equations JSONObject
     *
     * @param obj JSONObject for the equation data
     */
    private void checkVariables(final JSONObject obj) {
        final JSONArray variables = obj.optJSONArray(VARIABLES_KEY);
        Assert.assertNotNull("Variables is not an Array", variables);
        for (int i = 0; i < variables.length(); i++) {
            final JSONObject varObj = variables.optJSONObject(i);
            this.checkVariable(varObj);
        }
    }

    /**
     * Checks the given JSONObject representing a variable object
     *
     * @param varObj JSONObject representing a variable
     */
    private void checkVariable(final JSONObject varObj) {
        Assert.assertNotNull("Variable is not a JSONObject", varObj);
        Assert.assertTrue("Variable does not contain name", varObj.has(NAME_KEY));
        Assert.assertTrue("Equation does not contain symbol", varObj.has(SYMBOL_KEY));
        Assert.assertTrue("Equation does not contain expression", varObj.has(EXPRESSION_KEY));
        final String name = varObj.optString(NAME_KEY);
        Assert.assertNotNull("Variable name is not a String", name);
        final String symbol = varObj.optString(SYMBOL_KEY);
        Assert.assertNotNull("Variable symbol is not a String", symbol);
        final String expression = varObj.optString(EXPRESSION_KEY);
        Assert.assertNotNull("Variable expression is not a String", expression);
    }

    /**
     * Grabs all the contents of the given file and packs it into a string
     *
     * @param f File whose contents will be packed into a string
     * @return String containing the contents of the given file
     * @throws Exception I/O Exceptions
     */
    private String getFileAsString(final File f) throws Exception {
        try (final Scanner scanner = new Scanner(f)) {
            return scanner.useDelimiter("\\Z").next();
        }
    }
}
