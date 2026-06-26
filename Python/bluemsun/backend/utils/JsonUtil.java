package exam.bluemsun.backend.utils;

import com.alibaba.fastjson.JSONObject;
import jakarta.servlet.ServletInputStream;
import jakarta.servlet.http.HttpServletRequest;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;

/**
 * @author Deepwind
 */
public class JsonUtil {
    /**
     * 将接受到的输入流转换为 json 对象
     *
     * @param request HttpServletRequest
     * @return JSONObject
     */
    public static JSONObject getJson(HttpServletRequest request) {
        //从前端获取输入字节流
        ServletInputStream requestInputStream = null;
        try {
            requestInputStream = request.getInputStream();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
        //将字节流转换为字符流,并设置字符编码为utf-8
        InputStreamReader ir = null;
        try {
            ir = new InputStreamReader(requestInputStream, "utf-8");
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException(e);
        }
        //使用字符缓冲流进行读取
        BufferedReader br = new BufferedReader(ir);
        //开始拼装json字符串
        String line = null;
        StringBuilder sb = new StringBuilder();
        while (true) {
            try {
                if ((line = br.readLine()) == null) {
                    break;
                }
            } catch (IOException e) {
                throw new RuntimeException(e);
            }
            sb.append(line);
        }
        return JSONObject.parseObject(sb.toString());
    }
}
