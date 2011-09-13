using System;

using System.Collections.Generic;
using System.Text.RegularExpressions;

/*
    ChatterBotAPI
    Copyright (C) 2011 pierredavidbelanger@gmail.com
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Lesser General Public License for more details.

    You should have received a copy of the GNU Lesser General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
namespace ChatterBotAPI {
	
	class Cleverbot: ChatterBot {
		private readonly string url;
		
		public Cleverbot(string url) {
			this.url = url;
		}
		
		public ChatterBotSession CreateSession() {
			return new CleverbotSession(url);
		}
	}
	
	class CleverbotSession: ChatterBotSession {
		private static readonly Regex INPUT_HIDDEN_PATTERN = new Regex("<INPUT NAME=(.+?) TYPE=hidden VALUE=\"(.*?)\">", RegexOptions.IgnoreCase | RegexOptions.Multiline);
		private static readonly Regex EMOTION_AND_RESPONSE_PATTERN = new Regex("<!-- Begin Response !-->\\s*(?:\\{.+?,(.+?),.+?\\})*\\s*(.*?)\\s*<!-- End Response !-->", RegexOptions.IgnoreCase | RegexOptions.Multiline);
		
		private readonly string url;
		private readonly IDictionary<string, string> vars;
		
		public CleverbotSession(string url) {
			this.url = url;
			vars = new Dictionary<string, string>();
			vars["start"] = "y";
			vars["icognoid"] = "wsf";
			vars["fno"] = "0";
			vars["sub"] = "Say";
			vars["islearning"] = "1";
			vars["cleanslate"] = "false";
		}
		
		public ChatterBotThought Think(ChatterBotThought thought) {
			vars["stimulus"] = thought.Text;
			
			string formData = Utils.ParametersToWWWFormURLEncoded(vars);
			string formDataToDigest = formData.Substring(9, 20);
			string formDataDigest = Utils.MD5(formDataToDigest);
			vars["icognocheck"] = formDataDigest;
			
			string response = Utils.Post(url, vars);
			
			MatchCollection inputHiddenMatches = INPUT_HIDDEN_PATTERN.Matches(response);
			foreach (Match inputHiddenMatch in inputHiddenMatches) {
				GroupCollection inputHiddenGroups = inputHiddenMatch.Groups;
				string varName = inputHiddenGroups[1].Value.Trim();
				string varValue = inputHiddenGroups[2].Value.Trim();
				vars[varName] = varValue;
			}
			
			ChatterBotThought responseThought = new ChatterBotThought();
			
			Match emotionAndResponseMatch = EMOTION_AND_RESPONSE_PATTERN.Match(response);
			if (emotionAndResponseMatch.Success) {
				CaptureCollection emotionCaptures = emotionAndResponseMatch.Groups[1].Captures;
				responseThought.Emotions = new string[emotionCaptures.Count];
				for (int i = 0; i < emotionCaptures.Count; i++) {
					Capture emotionCapture = emotionCaptures[i];
					responseThought.Emotions[i] = emotionCapture.Value;
				}
				responseThought.Text = emotionAndResponseMatch.Groups[2].Value;
			}
			
			return responseThought;
		}
		
		public string Think(string text) {
			return Think(new ChatterBotThought() { Text = text }).Text;
		}
	}
}