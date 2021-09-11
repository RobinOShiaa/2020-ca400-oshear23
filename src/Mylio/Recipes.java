package com.example.mylio;

import com.google.gson.annotations.SerializedName;

public class Recipes {
    private String Ingredients;
    private String Instructions;
    private String Recipe_id;

    @SerializedName("body")
    private String text;


    public String getIngredients() {
        return Ingredients;
    }

    public String getInstructions() {
        return Instructions;
    }

    public String getRecipe_id() {
        return Recipe_id;
    }

    public String getText() {
        return text;
    }
}





