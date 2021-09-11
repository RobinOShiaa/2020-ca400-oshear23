package com.example.mylio;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.FirebaseFirestore;

import org.w3c.dom.Document;

import java.util.HashMap;
import java.util.Map;

public class RegisterActivity extends AppCompatActivity {
    EditText mTextUsername;
    EditText mTextPassword;
    FirebaseAuth fAuth;
    EditText getTextCnfPassword;
    Button mButtonRegister;
    TextView mTextViewLogin;
    ProgressBar progressBar;
    FirebaseFirestore fstore;
    String userid;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        mTextUsername = (EditText) findViewById(R.id.Username);
        mTextPassword = (EditText) findViewById(R.id.Password);
        getTextCnfPassword = (EditText) findViewById(R.id.cnf_Password);
        mButtonRegister = (Button) findViewById(R.id.Register);
        mTextViewLogin = (TextView) findViewById(R.id.textview_Register);
        fAuth = FirebaseAuth.getInstance();
        progressBar = findViewById(R.id.progressBar);

        if (fAuth.getCurrentUser() != null){
            startActivity(new Intent(RegisterActivity.this,HomeActivity.class));
            finish();

        }


        mTextViewLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent registerIntent = new Intent(RegisterActivity.this, LoginActivity.class);
                startActivity(registerIntent);
            }
        });


        mButtonRegister.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v){
                String username = mTextUsername.getText().toString().trim();
                String password = mTextPassword.getText().toString().trim();
                String cnfPassword = getTextCnfPassword.getText().toString().trim();

                if(TextUtils.isEmpty(username)){
                    mTextUsername.setError("Username is Required");
                    return;
                }
                if(TextUtils.isEmpty(password)){
                    mTextUsername.setError("Password is required");
                    return;
                }
                if(password.length() <= 5){
                    mTextPassword.setError("Password must be 6 or more characters");
                    return;
                }
                if(!password.equals(cnfPassword)) {
                    mTextPassword.setError("Password characters do not match");
                    return;
                }



                progressBar.setVisibility(View.VISIBLE);
                fAuth.createUserWithEmailAndPassword(username,password).addOnCompleteListener(new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) {
                        if(task.isSuccessful()){
                            Toast.makeText(RegisterActivity.this, "User Created", Toast.LENGTH_SHORT).show();
                            userid =  fAuth.getCurrentUser().getUid();
                            DocumentReference documentReference = fstore.collection("user_details").document(userid);
                            startActivity(new Intent(RegisterActivity.this,HomeActivity.class));
                        }
                        else{
                            Toast.makeText(RegisterActivity.this, "Error " + task.getException().getMessage(), Toast.LENGTH_SHORT).show();
                            return;
                        }
                    }
                });





            }
        });

    }
}