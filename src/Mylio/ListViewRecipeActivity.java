package com.example.mylio;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.ListView;

public class ListViewRecipeActivity extends AppCompatActivity {
    ListView lst;
    String [] recipes;
    String [] Instr;
    String [] Ing;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Intent intent = getIntent();
        Bundle extras = getIntent().getExtras();
        recipes = extras.getStringArray("recip");
        Instr = extras.getStringArray("Instruct");
        Ing = extras.getStringArray("Ingred");



        setContentView(R.layout.activity_list_view_recipe);
        lst = (ListView) findViewById(R.id.listviewrecipe);
        RecipeView rc = new RecipeView(this, recipes,Ing,Instr);
        lst.setAdapter(rc);

    }
}
