package com.example.mylio;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.CollectionReference;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FieldValue;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.protobuf.Any;

import java.io.File;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class Activity_Response <T> extends AppCompatActivity {
    public static final String msg = "TAG";
    private JsonPlaceHolderApi jsonPlaceHolderApi;
    private TextView textView1;
    private TextView textView2;
    private String text;
    private FirebaseAuth fAuth;
    public String TargetStore;
    private String userid;
    private DocumentReference DReference;
    private FirebaseFirestore fstore;
    private List<String> lstprod;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity__response);
        fAuth = FirebaseAuth.getInstance();
        fstore = FirebaseFirestore.getInstance();

        userid =  fAuth.getCurrentUser().getUid();
        DReference = fstore.collection("users").document(userid);

        Intent intent = getIntent();
        text = intent.getStringExtra(MainActivity.EXTRA_TEXT);

        textView1 = (TextView) findViewById(R.id.Store);
        textView2 = (TextView) findViewById(R.id.Products);


        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("https://df2e6c29.ngrok.io")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        jsonPlaceHolderApi = retrofit.create(JsonPlaceHolderApi.class);
        GetStore();


    }

    private void GetStore() {
        Call<List<Post>> call = jsonPlaceHolderApi.getPosts(text.split("_")[1]);
        call.enqueue(new Callback<List<Post>>() {
            @Override
            public void onResponse(Call<List<Post>> call, Response<List<Post>> response) {

                if (!response.isSuccessful()) {
                    textView1.setText("Code: " + response.code());
                    return;
                }

                List<Post> posts = response.body();

                for (Post post : posts) {
                    String content = "";
                    content += "Store id: " + post.getStoreid() + "\n";
                    TargetStore = post.getStoreid();

                    textView1.append(content);
                }
                System.out.println("====================================================================" + TargetStore + "=======================================================================");

                if(TargetStore.equals("Supervalu")){
                    GetSProducts();
                }
                if(TargetStore.equals("Aldi")){
                    GetAProducts();
                }
                if(TargetStore.equals("Tesco")){
                    GetTProducts();
                }
            }

            @Override
            public void onFailure(Call<List<Post>> call, Throwable t) {
                textView1.setText(t.getMessage());
            }
        });

    }

    private void GetSProducts() {

        SParser new1 = new SParser(text.split("_"));
        String SentProducts = new1.finalText;
        System.out.println("====================================================================" + SentProducts + "=======================================================================");
        SentProducts = new1.finalText.replace("null", "");
        Call<List<TProducts>> call = jsonPlaceHolderApi.GetSupervaluP(SentProducts);
        call.enqueue(new Callback<List<TProducts>>() {
            @Override
            public void onResponse(Call<List<TProducts>> call, Response<List<TProducts>> response) {

                if (!response.isSuccessful()) {
                    textView2.setText("Code: " + response.code());
                    return;
                }

                List<TProducts> sv = response.body();
                String content = "";
                for (TProducts prods : sv) {
                    if(content.contains(prods.getProduct_id() + "\n")){
                        continue;
                    }
                    else{
                        content += prods.getProduct_id() + "\n";
                    }
                }
                String lstinput [] = content.split("\n");
                List<String> prods = Arrays.asList(lstinput);
                lstprod = prods;
                AddProds();
                textView2.append(content);


            }

            @Override
            public void onFailure(Call<List<TProducts>> call, Throwable t) {
                textView2.setText(t.getMessage());
            }
        });
    }
    private void GetTProducts() {

        TParser new1 = new TParser(text.split("_"));
        System.out.print(text.charAt(0));
        String SentProducts = new1.finalText;
        System.out.println("====================================================================" + SentProducts + "=======================================================================");
        SentProducts = new1.finalText.replace("null", "");
        Call<List<TProducts>> call = jsonPlaceHolderApi.GetTescoP(SentProducts);
        call.enqueue(new Callback<List<TProducts>>() {
            @Override
            public void onResponse(Call<List<TProducts>> call, Response<List<TProducts>> response) {

                if (!response.isSuccessful()) {
                    textView2.setText("Code: " + response.code());
                    return;
                }

                List<TProducts> sv = response.body();
                String content = "";
                for (TProducts prods : sv) {
                    if(content.contains(prods.getProduct_id() + "\n")){
                        continue;
                    }
                    else{
                        content += prods.getProduct_id() + "\n";
                    }
                }
                String lstinput [] = content.split("\n");
                List<String> prods = Arrays.asList(lstinput);
                lstprod = prods;
                AddProds();
                textView2.append(content);

            }

            @Override
            public void onFailure(Call<List<TProducts>> call, Throwable t) {
                textView2.setText(t.getMessage());
            }
        });
    }

    private void GetAProducts() {

        AParser new1 = new AParser(text.split("_"));
        String SentProducts = new1.finalText;
        System.out.println("====================================================================" + SentProducts + "=======================================================================");
        SentProducts = new1.finalText.replace("null", "");
        Call<List<TProducts>> call = jsonPlaceHolderApi.GetAldiP(SentProducts);
        call.enqueue(new Callback<List<TProducts>>() {
            @Override
            public void onResponse(Call<List<TProducts>> call, Response<List<TProducts>> response) {

                if (!response.isSuccessful()) {
                    textView2.setText("Code: " + response.code());
                    return;
                }

                List<TProducts> sv = response.body();
                String content = "";
                for (TProducts prods : sv) {
                    if(content.contains(prods.getProduct_id() + "\n")){
                        continue;
                    }
                    else{
                        content += prods.getProduct_id() + "\n";
                    }
                }
                String lstinput [] = content.split("\n");
                List<String> prods = Arrays.asList(lstinput);
                lstprod = prods;
                AddProds();
                textView2.append(content);

            }

            @Override
            public void onFailure(Call<List<TProducts>> call, Throwable t) {
                textView2.setText(t.getMessage());
            }
        });
    }


    public void AddProds() {
        DReference.get().addOnCompleteListener(new OnCompleteListener<DocumentSnapshot>() {
            @Override
            public void onComplete(@NonNull Task<DocumentSnapshot> task) {
                if (task.isSuccessful()) {
                    DocumentSnapshot documentSnapshot = task.getResult();
                    if (documentSnapshot != null && documentSnapshot.exists()) {
                        Map<String, Object> map = documentSnapshot.getData();
                        Log.d("TAG", "DocumentSnapshot data: " + documentSnapshot.getData());
                        for(int index = 0; index <lstprod.size(); index ++){
                            DReference.update("Products", FieldValue.arrayUnion(lstprod.get(index)));

                        }


                    }
                    else {
                        Map<String, Object> user = new HashMap<>();
                        user.put("Products", lstprod);
                        DReference.set(user).addOnSuccessListener(new OnSuccessListener<Void>() {
                            @Override
                            public void onSuccess(Void aVoid) {
                                Log.d("TAG", "onSuccess: Products added for " + userid);
                            }
                        });

                    }
                }
            }
        });
    }
}
