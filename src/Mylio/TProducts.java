package com.example.mylio;
import com.google.gson.annotations.SerializedName;


public class TProducts {

    private String Image_Path;
    private String Image_Url;
    private String Product_id;

    @SerializedName("body")
    private String text;

    public String getImage_Path() {
        return Image_Path;
    }

    public String getImage_Url() {
        return Image_Url;
    }

    public String getProduct_id() {
        return Product_id;
    }

    public String getText() {
        return text;
    }
}