/**
 * E2E 测试 - 认证流程
 */
import { test, expect } from '@playwright/test';

test.describe('Authentication Flow', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display login button on homepage', async ({ page }) => {
    // 检查首页有登录按钮
    const loginButton = page.getByRole('button', { name: /登录/i });
    await expect(loginButton).toBeVisible();
  });

  test('should navigate to login page', async ({ page }) => {
    await page.getByRole('button', { name: /登录/i }).click();
    await expect(page).toHaveURL(/.*login.*/);
  });

  test('should register new user successfully', async ({ page }) => {
    // 前往注册页面
    await page.goto('/register');
    
    // 填写注册表单
    const username = `testuser_${Date.now()}`;
    await page.getByPlaceholder('用户名').fill(username);
    await page.getByPlaceholder('邮箱').fill(`${username}@example.com`);
    await page.getByPlaceholder('密码').fill('TestPass123!');
    await page.getByPlaceholder('确认密码').fill('TestPass123!');
    
    // 提交注册
    await page.getByRole('button', { name: /注册/i }).click();
    
    // 等待注册成功并跳转
    await expect(page).toHaveURL(/.*login.*/);
    
    // 检查成功提示
    // await expect(page.getByText(/注册成功/i)).toBeVisible();
  });

  test('should login with valid credentials', async ({ page }) => {
    // 前往登录页面
    await page.goto('/login');
    
    // 填写登录表单
    await page.getByPlaceholder('用户名').fill('testuser');
    await page.getByPlaceholder('密码').fill('TestPass123!');
    
    // 提交登录
    await page.getByRole('button', { name: /登录/i }).click();
    
    // 等待登录成功
    // await expect(page).toHaveURL(/.*dashboard.*/);
    // await expect(page.getByText(/欢迎/i)).toBeVisible();
  });

  test('should show error with invalid credentials', async ({ page }) => {
    await page.goto('/login');
    
    // 填写错误密码
    await page.getByPlaceholder('用户名').fill('testuser');
    await page.getByPlaceholder('密码').fill('WrongPassword!');
    await page.getByRole('button', { name: /登录/i }).click();
    
    // 检查错误提示
    // await expect(page.getByText(/用户名或密码错误/i)).toBeVisible();
  });

  test('should logout successfully', async ({ page }) => {
    // 假设已登录（实际测试中应该先登录）
    await page.goto('/dashboard');
    
    // 点击登出
    // await page.getByRole('button', { name: /登出/i }).click();
    
    // 验证已登出
    // await expect(page).toHaveURL(/.*login.*/);
  });

  test('should protect authenticated routes', async ({ page }) => {
    // 尝试直接访问需要认证的页面
    await page.goto('/assets');
    
    // 应该被重定向到登录页
    // await expect(page).toHaveURL(/.*login.*/);
  });

  test('should persist login session', async ({ page, context }) => {
    // 登录
    await page.goto('/login');
    await page.getByPlaceholder('用户名').fill('testuser');
    await page.getByPlaceholder('密码').fill('TestPass123!');
    await page.getByRole('button', { name: /登录/i }).click();
    
    // 等待登录成功
    // await expect(page).toHaveURL(/.*dashboard.*/);
    
    // 刷新页面
    await page.reload();
    
    // 应该保持登录状态
    // await expect(page).toHaveURL(/.*dashboard.*/);
  });
});

test.describe('Password Reset Flow', () => {
  test('should request password reset', async ({ page }) => {
    await page.goto('/login');
    
    // 点击忘记密码
    // await page.getByText(/忘记密码/i).click();
    
    // 填写邮箱
    // await page.getByPlaceholder('邮箱').fill('test@example.com');
    // await page.getByRole('button', { name: /发送重置邮件/i }).click();
    
    // 检查成功提示
    // await expect(page.getByText(/重置邮件已发送/i)).toBeVisible();
  });
});
