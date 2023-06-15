package com.ykbintang.envy.views.setting

import android.content.Intent
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.appcompat.app.AppCompatActivity
import com.ykbintang.envy.R
import com.ykbintang.envy.Utils
import com.ykbintang.envy.Utils.setAppLocale
import com.ykbintang.envy.databinding.FragmentSettingBinding
import com.ykbintang.envy.views.MainActivity

class SettingFragment : Fragment() {
    private lateinit var binding: FragmentSettingBinding

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View {
        binding = FragmentSettingBinding.inflate(layoutInflater)
        return binding.root
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

        binding.btnNightMode.setOnClickListener {
            val isNightMode = Utils.getIsDarkMode(requireContext())
            Utils.setIsDarkMode(requireContext(), !isNightMode)
        }
        binding.btnLanguage.setOnClickListener {
            val pref = requireActivity().getSharedPreferences("main", AppCompatActivity.MODE_PRIVATE)
            var localeValue = pref.getString("locale", "in")

            localeValue = if(localeValue == "in") {
                "en"
            } else {
                "in"
            }

            pref.edit().putString("locale", localeValue).apply()
            requireContext().setAppLocale(localeValue)

            Intent(requireContext(), MainActivity::class.java).also {
                startActivity(it)
            }
            requireActivity().finish()
        }
    }
}