package com.example.mylio;

import java.util.List;

import retrofit2.Call;
import retrofit2.http.GET;
import retrofit2.http.Query;

public interface JsonPlaceHolderApi {

    @GET("get_store")
    Call<List<Post>> getPosts(@Query("Store") String Store);

    @GET("Supervalue/Query")
    Call<List<TProducts>> GetSupervaluP(@Query("Products") String P);

    @GET("Tesco/Query")
    Call<List<TProducts>> GetTescoP(@Query("Products") String P);

    @GET("Aldi/Query")
    Call<List<TProducts>> GetAldiP(@Query("Products") String P);

    @GET("recipes")
    Call<List<Recipes>> GetRecipes(@Query("Products") String P);
}
