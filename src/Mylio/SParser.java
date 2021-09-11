package com.example.mylio;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

public class SParser {

    static String Store;
    static String [] ListText;
    static String finalText;

    public SParser(String[] text){
        ListText = text;
        SParser.Parse();

    }

    public static String[] getListText() {
        return ListText;
    }

    public static void Parse() {
        String word = "";
        for (int i = 7; i < ListText.length; i++) {

            if(ListText[i].length() > 4 || !ListText[i].equals("")){

                if (ListText[i].contains("Tota")) {
                    break;
                }
                if (isPricing(ListText[i])) {
                    continue;
                }

                else {
                    ListText[i] = ListText[i].replaceAll("\\d","");
                    word = word + ListText[i] + ",";
                }
                if (i == ListText.length - 1){
                    word = word + ListText[i];
                }


            }
        }
        finalText = word;
    }

    public static boolean isPricing(String inputText)
    {
        String regExPattern = "(|e|-|EUR|€|E|)\\s?(\\d{1,3}(?:[.,]\\d{3})*(?:[.,]\\d{2}))|(\\d{1,3}(?:[.,]\\d{3})*(?:[.,]\\d{2})?)\\s?(|-|EUR|€|E|e|)";
        boolean matches = false;
        matches = Pattern.matches(regExPattern,inputText);
        if(matches){
            return true;
        }
        return false;
    }
}



