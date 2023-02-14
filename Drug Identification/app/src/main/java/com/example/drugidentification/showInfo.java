package com.example.drugidentification;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.widget.TextView;

public class showInfo extends AppCompatActivity {
    String info;
    TextView showTxt;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_info);


        Intent i = getIntent();
        Bundle b = i.getExtras();

        info = b.getString("info");

        showTxt.setText(info);

    }
}