package com.example.mylio;

import java.util.regex.Pattern;

public class TParser {
    static String Store;
    static String[] ListText;
    static String finalText;


    public TParser(String[] text) {
        Store = text[0];
        ListText = text;
        TParser.Parse();

    }

    public static void Parse() {
        String word = "";
        for (int i = 4; i < ListText.length; i++) {
            if (ListText[i].length() == 1){
                continue;
            }

            if(ListText[i].contains("EUR")){
                continue;
            }
            if (ListText[i].equals("TOTAL")){
                break;
            }

            else{
                System.out.println("================" + ListText[i] + "=====================");
                word += ListText[i] + ",";
            }


        }
        String result = word.substring(0, word.length() - 1);

        finalText = result;
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