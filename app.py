from flask import Flask, render_template, request, redirect
import sqlite3 as sql
import pandas as pd

app = Flask(__name__)