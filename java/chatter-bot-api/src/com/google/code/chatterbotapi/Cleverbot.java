package com.google.code.chatterbotapi;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/*
    chatter-bot-api
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
class Cleverbot implements ChatterBot {
    private static final Pattern INPUT_HIDDEN_PATTERN = Pattern.compile("<INPUT NAME=(.+?) TYPE=hidden VALUE=\"(.*?)\">", Pattern.CASE_INSENSITIVE | Pattern.MULTILINE);
    private static final Pattern EMOTION_AND_RESPONSE_PATTERN = Pattern.compile("<!-- Begin Response !-->\\s*(?:\\{.+?,(.+?),.+?\\})*\\s*(.*)\\s*<!-- End Response !-->", Pattern.CASE_INSENSITIVE | Pattern.MULTILINE);

    private final String url;

    public Cleverbot(String url) {
        this.url = url;
    }

    @Override
    public ChatterBotSession createSession() {
        return new Session();
    }
    
    private class Session implements ChatterBotSession {
        private final Map<String, String> vars;

        public Session() {
            vars = new LinkedHashMap<String, String>();
            vars.put("start", "y");
            vars.put("icognoid", "wsf");
            vars.put("fno", "0");
            vars.put("sub", "Say");
            vars.put("islearning", "1");
            vars.put("cleanslate", "false");
        }
        
        @Override
        public ChatterBotThought think(ChatterBotThought thought) throws Exception {
            vars.put("stimulus", thought.getText());

            String formData = Utils.parametersToWWWFormURLEncoded(vars);
            String formDataToDigest = formData.substring(9, 29);
            String formDataDigest = Utils.md5(formDataToDigest);
            vars.put("icognocheck", formDataDigest);

            String response = Utils.post(url, vars);
            
            Matcher inputHiddenMatcher = INPUT_HIDDEN_PATTERN.matcher(response);
            while (inputHiddenMatcher.find()) {
                String varName = inputHiddenMatcher.group(1);
                String varValue = inputHiddenMatcher.group(2);
                vars.put(varName.trim(), varValue.trim());
            }

            ChatterBotThought responseThought = new ChatterBotThought();

            Matcher emotionAndResponseMatcher = EMOTION_AND_RESPONSE_PATTERN.matcher(response);
            if (emotionAndResponseMatcher.find()) {
                //TODO: parse emotions
                responseThought.setText(emotionAndResponseMatcher.group(emotionAndResponseMatcher.groupCount()).trim());
            }
            
            return responseThought;
        }

        @Override
        public String think(String text) throws Exception {
            ChatterBotThought thought = new ChatterBotThought();
            thought.setText(text);
            return think(thought).getText();
        }
    }
}