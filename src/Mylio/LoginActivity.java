package com.example.mylio;
import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.content.Intent;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.auth.AuthResult;
import com.google.firebase.auth.FirebaseAuth;


public class LoginActivity extends AppCompatActivity {
    EditText mTextUsername;
    EditText mTextPassword;
    Button mButtonLogin;
    ProgressBar progressBar;
    FirebaseAuth fAuth;
    TextView mTextViewRegister;
    //DatabaseHelper db;
    ViewGroup progressView;
    protected boolean isProgressShowing = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);

        //db = new DatabaseHelper(this);
        mTextUsername = (EditText) findViewById(R.id.Username);///username
        mTextPassword = (EditText) findViewById(R.id.Password);//password
        mButtonLogin = (Button) findViewById(R.id.Login);//login button
        mTextViewRegister = (TextView) findViewById(R.id.Register);//register
        progressBar = findViewById(R.id.progressBar2); //bar that loads while login
        fAuth = FirebaseAuth.getInstance(); //connect
        mTextViewRegister.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Intent registerIntent = new Intent(LoginActivity.this, RegisterActivity.class);
                startActivity(registerIntent);
            }
        });




        mButtonLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) { //listen for click on button
                String username = mTextUsername.getText().toString().trim(); //set username and password values
                String password = mTextPassword.getText().toString().trim();

                if (TextUtils.isEmpty(username)) {
                    mTextUsername.setError("Username is Required");
                    return;
                }
                if (TextUtils.isEmpty(password)) {
                    mTextUsername.setError("Password is required");
                    return;
                }
                if (password.length() < 6) {
                    mTextPassword.setError("Password must be 6 or more characters");
                    return;
                }

                progressBar.setVisibility(View.VISIBLE); //progress bar appears
                fAuth.signInWithEmailAndPassword(username,password).addOnCompleteListener(new OnCompleteListener<AuthResult>() {
                    @Override
                    public void onComplete(@NonNull Task<AuthResult> task) { //attempt to sign in with email and password
                        if(task.isSuccessful()){
                            Toast.makeText(LoginActivity.this, "Login Succesful", Toast.LENGTH_SHORT).show();
                            startActivity(new Intent(LoginActivity.this,HomeActivity.class));
                        }
                        else{
                            Toast.makeText(LoginActivity.this, "Error " + task.getException().getMessage(), Toast.LENGTH_SHORT).show();
                        }
                    }
                });
            }
        });

    }
}
