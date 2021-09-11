package com.example.mylio;
import java.util.List;
import com.google.firebase.firestore.Exclude;

public class Produce {
    List <String> Prodid;

    public Produce(){

    }

    public Produce(List<String> tags){
        this.Prodid = tags;
    }

    public void setProdid(List<String> prodid) {
        Prodid = prodid;
    }

    public List<String> getProdid() {
        return Prodid;
    }
}
