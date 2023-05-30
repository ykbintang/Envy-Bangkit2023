package com.ykbintang.envy

import android.content.Context
import android.content.Context.MODE_PRIVATE
import android.content.res.Configuration
import android.os.Build
import android.util.Log
import androidx.annotation.RequiresApi
import androidx.appcompat.app.AppCompatDelegate
import java.io.File
import java.io.FileInputStream
import java.io.FileNotFoundException
import java.io.IOException
import java.text.SimpleDateFormat
import java.util.*

object Utils {
    fun formatCurrentDate(): String {
        val format = SimpleDateFormat("dd MMMM yyyy, HH:mm", Locale.getDefault())
        return format.format(Date())
    }

    fun formattedMillisDate(
        pattern: String?,
        date: Date?
    ): String {
        val format = SimpleDateFormat(pattern, Locale.getDefault())
        return format.format(date)
    }

    @RequiresApi(Build.VERSION_CODES.O)
    fun encodeFileToBase64Binary(path: String?): String {
        var base64File = ""
        val file = File(path)
        try {
            FileInputStream(file).use { imageInFile ->
                val fileData = ByteArray(file.length().toInt())
                imageInFile.read(fileData)
                base64File = Base64.getEncoder().encodeToString(fileData)
            }
        } catch (e: FileNotFoundException) {
            Log.d("TAG", e.message!!)
        } catch (ioe: IOException) {
            Log.d("TAG", "Exception while reading the file $ioe")
        }
        return base64File
    }

    fun setIsDarkMode(context: Context, isNight: Boolean) {
        val pref = context.getSharedPreferences("main", MODE_PRIVATE)
        pref.edit().putBoolean("isNight", isNight).apply()

        if(isNight) AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_YES)
        else AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO)
    }

    fun getIsDarkMode(context: Context): Boolean {
        val pref = context.getSharedPreferences("main", MODE_PRIVATE)
        return pref.getBoolean("isNight", false)
    }

    fun setLanguage(context: Context, localeValue: String) {
        val pref = context.getSharedPreferences("main", MODE_PRIVATE)
        pref.edit().putString("locale", localeValue).apply()

        val locale = Locale(localeValue)
        Locale.setDefault(locale)
        val config = Configuration()
        config.locale = locale
        context.applicationContext.resources.updateConfiguration(config, null)
    }

    fun Context.setAppLocale(language: String): Context {
        val locale = Locale(language)
        Locale.setDefault(locale)
        val config = resources.configuration
        config.setLocale(locale)
        config.setLayoutDirection(locale)
        return createConfigurationContext(config)
    }
}