package com.example.mylio;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FirebaseFirestore;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class HomeActivity extends AppCompatActivity {
    Button Repobtn;
    Button Scanbtn;
    Button Recipebtn;
    private JsonPlaceHolderApi jsonPlaceHolderApi;
    public static String idproducts = "userp";
    public static String idrecipes = "recip";
    public static String idInstructions = "Ingred";
    public static String idIngredients = "Instruct";
    FirebaseAuth fAuth;
    FirebaseFirestore fstore;
    String userId;
    Button Viewbtn;
    String [] sentProds;
    String [] sentRecipes;
    String [] sentInstructions;
    String [] sentIngredients;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);
        Scanbtn = (Button) findViewById(R.id.Scanner);
        Repobtn = (Button) findViewById(R.id.Repo);
        Recipebtn = (Button) findViewById(R.id.Recipes);

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("https://df2e6c29.ngrok.io")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        jsonPlaceHolderApi = retrofit.create(JsonPlaceHolderApi.class);
        GetUserProds();






        Scanbtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(HomeActivity.this, MainActivity.class);
                startActivity(intent);
            }
        });

        Repobtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(HomeActivity.this, ListViewActivity.class);

                intent.putExtra(idproducts,sentProds);
                startActivity(intent);
            }
        });

        Recipebtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent intent = new Intent(HomeActivity.this, ListViewRecipeActivity.class);
                intent.putExtra(idrecipes,sentRecipes);
                intent.putExtra(idIngredients,sentIngredients);
                intent.putExtra(idInstructions,sentInstructions);
                startActivity(intent);
            }
        });


    }

    public void logout(View view){
        FirebaseAuth.getInstance().signOut();
        startActivity(new Intent(HomeActivity.this,LoginActivity.class));
    }

    public void GetUserProds(){
        fAuth = FirebaseAuth.getInstance();
        fstore = FirebaseFirestore.getInstance();
        userId =  fAuth.getCurrentUser().getUid();
        DocumentReference DC = fstore.collection("users").document(userId);
        fstore.collection("users").document(userId).get().addOnCompleteListener(new OnCompleteListener<DocumentSnapshot>() {
            @Override
            public void onComplete(@NonNull Task<DocumentSnapshot> task) {
                if (task.isSuccessful()) {
                    DocumentSnapshot document = task.getResult();
                    if (document.exists()) {
                        List<String> list = (List<String>) document.get("Products");
                        String products [] = new String[list.size()];
                        String [] list1 = list.toArray(products);
                        sentProds = list1;
                        RetrieveRecipes();
                    }
                }
            }
        });
    }


    private void RetrieveRecipes() {

        if(sentProds != null) {
            System.out.println(sentProds.toString());
            String msg = "";
            for (int i = 0; i < sentProds.length; i++) {
                if (i == sentProds.length - 1) {
                    msg += sentProds[i];
                }
                else{
                    msg += sentProds[i] + ",";

                }
            }
            String SentProducts = msg;
            System.out.println("Send Products =================================================================" + SentProducts + "=======================================================================");
            Call<List<Recipes>> call = jsonPlaceHolderApi.GetRecipes(SentProducts);
            call.enqueue(new Callback<List<Recipes>>() {
                @Override
                public void onResponse(Call<List<Recipes>> call, Response<List<Recipes>> response) {
                    if (!response.isSuccessful()) {
                        Toast.makeText(HomeActivity.this, "recipes not recieved", Toast.LENGTH_SHORT).show();
                        return;
                    }

                    List<Recipes> sv = response.body();
                    String contentR = "";
                    String contentIng = "";
                    String contentInstr = "";
                    for (Recipes re : sv) {
                        contentR += re.getRecipe_id() + "\n";
                        contentIng += re.getIngredients() + "\n";
                        contentInstr += re.getInstructions() + "\n";

                    }

                    sentRecipes = contentR.split("\n");
                    sentIngredients = contentIng.split("\n");
                    sentInstructions = contentInstr.split("\n");

                }
                @Override
                public void onFailure(Call<List<Recipes>> call, Throwable t) {
                    Toast.makeText(HomeActivity.this, "No recipes recieved", Toast.LENGTH_SHORT).show();
                }
            });
        }
        else{
            System.out.println("=============================is null==========================");
        }
    }

}
