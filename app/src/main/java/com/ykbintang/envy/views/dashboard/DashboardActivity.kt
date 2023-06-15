package com.ykbintang.envy.views.dashboard

import android.content.Context
import android.content.ContextWrapper
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.PersistableBundle
import androidx.fragment.app.Fragment
import com.ykbintang.envy.R
import com.ykbintang.envy.Utils.setAppLocale
import com.ykbintang.envy.databinding.ActivityDashboardBinding
import com.ykbintang.envy.views.home.HomeFragment
import com.ykbintang.envy.views.article.ArticleFragment
import com.ykbintang.envy.views.setting.SettingFragment

class DashboardActivity : AppCompatActivity() {
    private  lateinit var binding: ActivityDashboardBinding
    private var currentItem = 0

    override fun attachBaseContext(newBase: Context) {
        val pref = newBase.getSharedPreferences("main", MODE_PRIVATE)
        val localeValue = pref.getString("locale", "in")
        super.attachBaseContext(ContextWrapper(newBase.setAppLocale(localeValue!!)))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        binding = ActivityDashboardBinding.inflate(layoutInflater)
        setContentView(binding.root)

        val item = savedInstanceState?.getInt("item")
        if(item != null) {
            moveFragment(SettingFragment())
        } else {
            moveFragment(HomeFragment())
        }

        binding.botNav.setOnItemSelectedListener {
            currentItem = when (it.itemId) {
                R.id.menu_home -> {
                    moveFragment(HomeFragment())
                    0
                }
                R.id.menu_library -> {
                    moveFragment(ArticleFragment())
                    1
                }
                else -> {
                    moveFragment(SettingFragment())
                    2
                }
            }

            true
        }
    }

    override fun onSaveInstanceState(outState: Bundle, outPersistentState: PersistableBundle) {
        super.onSaveInstanceState(outState, outPersistentState)
        outState.putInt("item", currentItem)
    }

    private fun moveFragment(fragment: Fragment) {
        supportFragmentManager.beginTransaction().replace(R.id.fragment_container, fragment).commit()
    }
}