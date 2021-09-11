package com.example.mylio;
import android.app.Activity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.TextView;
import androidx.annotation.NonNull;
import androidx.annotation.Nullable;

public class RecipeView extends ArrayAdapter {
    private String [] Recipes;
    private String [] Instructions;
    private String [] Ingredients;
    private Activity context;

    public RecipeView(Activity context, String[] Recipes, String [] Ingredients,String [] Instructions ){
        super(context,R.layout.listview_layout,Recipes);
        this.context = context;
        this.Recipes = Recipes;
        this.Instructions = Instructions;
        this.Ingredients = Ingredients;

    }

    @NonNull
    @Override
    public View getView(int position, @Nullable View convertView, @NonNull ViewGroup parent){
        View r = convertView;
        RecipeView.ViewHolder2 viewHolder = null;
        if(r==null){
            LayoutInflater layoutInflater = context.getLayoutInflater();
            r = layoutInflater.inflate(R.layout.listview_layout2,null,true);
            viewHolder = new ViewHolder2(r);
            r.setTag(viewHolder);

        }
        else{
            viewHolder = (ViewHolder2) r.getTag();
        }
        viewHolder.tv1.setText(Recipes[position]);
        viewHolder.tv2.setText(Ingredients[position]);
        viewHolder.tv3.setText(Instructions[position]);

        return r;
    }

    class ViewHolder2 {
        TextView tv1;
        TextView tv2;
        TextView tv3;

        ViewHolder2(View v) {
            tv1 = (TextView) v.findViewById(R.id.recipename);
            tv2 = (TextView) v.findViewById(R.id.Ingred);
            tv3 = (TextView) v.findViewById(R.id.Instruc);
        }
    }
}