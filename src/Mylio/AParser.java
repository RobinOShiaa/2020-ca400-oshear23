package com.example.mylio;

import java.util.regex.Pattern;

public class AParser {
    static String Store;
    static String[] ListText;
    static String finalText;


    public AParser(String[] text) {
        Store = text[1];
        ListText = text;
        AParser.Parse();

    }

    public static void Parse() {
        String word = "";
        for (int i = 5; i < ListText.length; i++) {


            if (isPricing(ListText[i])) {
                continue;
            }

            if (isIdNum(ListText[i].split(" ")[0])){
                String newText = ListText[i].replace(ListText[i].split(" ")[0],"");
                word = word + newText.replaceAll("^\\s+", "") + ",";
            }

        }

        String result = word.substring(0, word.length() - 1);

        finalText = result;
        System.out.println(finalText);
    }

    public static boolean isPricing(String inputText) {
        String regExPattern = "(\\d{1,3}(?:[.,]\\d{3})*(?:[.,]\\d{2}))|(\\d{1,3}(?:[.,]\\d{3})*(?:[.,]\\d{2})?)\\s?([a-zA-Z])";
        boolean matches = false;
        matches = Pattern.matches(regExPattern, inputText);
        if (matches) {
            return true;
        }
        return false;
    }
    public static boolean isIdNum(String inputText) {
        String regExPattern = "(?:(^([0-9])+))";
        boolean matches = false;
        matches = Pattern.matches(regExPattern, inputText);
        if (matches) {
            return true;
        }
        return false;
    }

    public static String getStore() {
        return Store;
    }

    public static String[] getListText() {
        return ListText;
    }

    public static String getFinalText() {
        return finalText;
    }
}