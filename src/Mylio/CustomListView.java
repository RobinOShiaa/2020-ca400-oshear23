package com.example.mylio;

import android.app.Activity;
import android.content.Context;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;

import androidx.annotation.LayoutRes;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

public class CustomListView extends ArrayAdapter {
    private String [] prodname;
    private Activity context;

    public CustomListView(Activity context, String[] prodname){
        super(context,R.layout.listview_layout,prodname);
        this.context = context;
        this.prodname = prodname;

    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent){
        View r = convertView;
        ViewHolder viewHolder = null;
        if(r==null){
            LayoutInflater layoutInflater = context.getLayoutInflater();
            r = layoutInflater.inflate(R.layout.listview_layout,null,true);
            viewHolder = new ViewHolder(r);
            r.setTag(viewHolder);

        }
        else{
            viewHolder = (ViewHolder) r.getTag();
    }
        viewHolder.tv1.setText(prodname[position]);

        return r;
    }

    class ViewHolder{
        TextView tv1;
        ViewHolder(View v){
            tv1 = (TextView) v.findViewById(R.id.prodname);
        }
    }



}
