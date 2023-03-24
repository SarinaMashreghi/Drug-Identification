package com.example.drugidentification;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.content.Intent;
import android.os.Bundle;
import android.widget.TextView;

public class showSummary extends AppCompatActivity {
    TextView sum_txt;

    @SuppressLint("MissingInflatedId")
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_show_summary);
        sum_txt = findViewById(R.id.summary_view);

        Intent i = getIntent();
        Bundle b = i.getExtras();

        String summary_text = b.getString("summary");
        sum_txt.setText(summary_text);
    }
}