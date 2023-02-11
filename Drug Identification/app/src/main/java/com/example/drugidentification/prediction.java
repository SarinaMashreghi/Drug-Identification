package com.example.drugidentification;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.TextView;

public class prediction extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_prediction);

        TextView predTxt = findViewById(R.id.pred_txt);
        TextView accTxt = findViewById(R.id.acc_txt);
//        link = findViewById(R.id.link);

//        link.setMovementMethod(LinkMovementMethod.getInstance());

        Intent i = getIntent();
        Bundle b = i.getExtras();

        String pred = b.getString("prediction");
        float acc = b.getFloat("accuracy");

//        predTxt.setText("Predicted Letter: W");
//        accTxt.setText("Accuracy: 92%");
        predTxt.setText("Predicted Letter: "+pred);
        accTxt.setText("Accuracy: "+ String.valueOf(acc));
    }
}