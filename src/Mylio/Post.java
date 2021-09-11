package com.example.mylio;

import com.google.gson.annotations.SerializedName;


public class Post {

    private String Store;

    @SerializedName("body")
    private String text;

    public String getStoreid() {
        return Store;
    }

}