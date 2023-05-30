package com.ykbintang.envy.views

import android.content.Context
import android.content.ContextWrapper
import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import androidx.appcompat.app.AppCompatDelegate
import androidx.lifecycle.lifecycleScope
import com.ykbintang.envy.R
import com.ykbintang.envy.Utils
import com.ykbintang.envy.Utils.setAppLocale
import com.ykbintang.envy.views.dashboard.DashboardActivity
import kotlinx.coroutines.delay
import kotlinx.coroutines.launch

class MainActivity : AppCompatActivity() {

    override fun attachBaseContext(newBase: Context) {
        val pref = newBase.getSharedPreferences("main", MODE_PRIVATE)
        val localeValue = pref.getString("locale", "in")
        super.attachBaseContext(ContextWrapper(newBase.setAppLocale(localeValue ?: "in")))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        val isNight = Utils.getIsDarkMode(this)
        if(isNight) AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_YES)
        else  AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO)

        setContentView(R.layout.activity_main)

        lifecycleScope.launch {
            delay(2000)

            Intent(this@MainActivity, DashboardActivity::class.java).also {
                startActivity(it)
                finish()
            }
        }
    }
}