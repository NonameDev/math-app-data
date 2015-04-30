package mathapp.datachecker;

import org.json.JSONArray;
import org.json.JSONObject;
import org.junit.Assert;

import java.io.File;
import java.util.Scanner;

import static mathapp.datachecker.Constants.*;

/**
 */
public class DataChecker {

    private String eqnDataPath;
    private String versionPath;


    public DataChecker() {
        this(REAL_DATA_PATH);
    }

    public DataChecker(final String dataPath) {
        this.eqnDataPath = dataPath + EQN_DATA_FILE_NAME;
        this.versionPath = dataPath + VERSION_FILE_NAME;
    }

    public void validateData() throws Exception {
        final File eqnDataFile = new File(this.eqnDataPath);
        final File versionFile = new File(this.versionPath);
        this.checkFilesExist(eqnDataFile, versionFile);
        final String eqnDataString = this.getFileAsString(eqnDataFile);
        final String versionString = this.getFileAsString(versionFile);
        this.validateVersionFile(versionString);
        this.validateEquationData(eqnDataString);
    }


    private void checkFilesExist(final File eqnDataFile, final File versionFile) {
        Assert.assertTrue("Equation data file does not exit", eqnDataFile.isFile());
        Assert.assertTrue("Version file does not exit", versionFile.isFile());
    }

    private void validateEquationData(final String content) throws Exception {
        final JSONObject baseJsonObject = new JSONObject(content);
        Assert.assertTrue("Equation data does not contain equations", baseJsonObject.has(EQUATIONS_KEY));
        final JSONArray eqnsArray = baseJsonObject.optJSONArray(EQUATIONS_KEY);
        Assert.assertNotNull("Equarions is not an array", eqnsArray);
        for (int i = 0; i < eqnsArray.length(); i++) {
            this.checkEquationJsonObject(eqnsArray.optJSONObject(i));
        }
    }

    private void checkEquationJsonObject(final JSONObject obj) {
        Assert.assertNotNull("Equation is not a JSONObject", obj);
        Assert.assertTrue("Equation does not contain name", obj.has(NAME_KEY));
        Assert.assertTrue("Equation does not contain keywords", obj.has(KEYWORDS_KEY));
        Assert.assertTrue("Equation does not contain variables", obj.has(VARIABLES_KEY));
        this.checkName(obj);
        this.checkKeywords(obj);
        this.checkVariables(obj);
    }

    private void checkName(final JSONObject obj) {
        final String name = obj.optString(NAME_KEY);
        Assert.assertNotNull("Name is not a String", name);
    }

    private void checkKeywords(final JSONObject obj) {
        final JSONArray keywords = obj.optJSONArray(KEYWORDS_KEY);
        Assert.assertNotNull("Keywords is not an array", keywords);
        for (int i = 0; i < keywords.length(); i++) {
            final String keyword = keywords.optString(i);
            Assert.assertNotNull("Keywords is not a String", keyword);
        }
    }

    private void checkVariables(final JSONObject obj) {
        final JSONArray variables = obj.optJSONArray(VARIABLES_KEY);
        Assert.assertNotNull("Variables is not an Array", variables);
        for (int i = 0; i < variables.length(); i++) {
            final JSONObject varObj = variables.optJSONObject(i);
            this.checkVariable(varObj);
        }
    }

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

    private void validateVersionFile(final String content) throws Exception {
        final JSONObject baseJsonObject = new JSONObject(content);
        Assert.assertTrue("Version data does not contain version", baseJsonObject.has(VERSION_KEY));
        final int versionNum = baseJsonObject.optInt(VERSION_KEY, -1);
        Assert.assertTrue("Version is not an int", versionNum != -1);
    }

    private String getFileAsString(final File f) throws Exception {
        try (final Scanner scanner = new Scanner(f)) {
            return scanner.useDelimiter("\\Z").next();
        }
    }
}
