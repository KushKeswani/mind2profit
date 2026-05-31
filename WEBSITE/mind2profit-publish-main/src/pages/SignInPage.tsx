import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/hooks/use-toast";
import { useAuth } from "@/contexts/AuthContext";

const SignInPage = () => {
  const { login, requestPasswordReset, isAuthenticated, isSubscribed, isLoading } = useAuth();
  const navigate = useNavigate();
  const { toast } = useToast();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isResetting, setIsResetting] = useState(false);

  useEffect(() => {
    if (isLoading) return;
    if (isAuthenticated) {
      navigate(isSubscribed ? "/dashboard" : "/");
    }
  }, [isAuthenticated, isSubscribed, isLoading, navigate]);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!email || !password) {
      toast({
        title: "Missing Fields",
        description: "Enter your email and password to continue.",
        variant: "destructive",
      });
      return;
    }

    setIsSubmitting(true);
    try {
      await login(email, password);
      toast({
        title: "Signed In",
        description: "Welcome back.",
      });
    } catch (error) {
      toast({
        title: "Sign-in Failed",
        description: "Invalid email or password.",
        variant: "destructive",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleForgotPassword = async () => {
    if (!email) {
      toast({
        title: "Email Required",
        description: "Enter your account email first, then click forgot password.",
        variant: "destructive",
      });
      return;
    }
    setIsResetting(true);
    try {
      await requestPasswordReset(email);
      toast({
        title: "Reset Email Sent",
        description: "Check your inbox for password reset instructions.",
      });
    } catch (error: any) {
      toast({
        title: "Reset Failed",
        description: error?.message || "Unable to send reset email.",
        variant: "destructive",
      });
    } finally {
      setIsResetting(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
      <Card className="w-full max-w-md bg-white/5 border-white/10 text-white">
        <CardHeader className="space-y-2">
          <Badge variant="secondary" className="w-fit bg-purple-100 text-purple-800">
            Secure Access
          </Badge>
          <CardTitle>Sign in to Mind2Profit</CardTitle>
          <CardDescription className="text-gray-300">
            Access your journal, coaching, and dashboard once your subscription is active.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="bg-white/10 border-white/20 text-white"
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="bg-white/10 border-white/20 text-white"
                required
              />
            </div>
            <Button
              type="submit"
              disabled={isSubmitting}
              className="w-full bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600"
            >
              {isSubmitting ? "Signing in..." : "Sign In"}
            </Button>
          </form>

          <p className="text-sm text-gray-300 mt-4 text-center">
            New here? <Link to="/signup" className="text-purple-300 hover:text-purple-200">Create an account</Link>.
          </p>
          <button
            type="button"
            onClick={handleForgotPassword}
            disabled={isResetting}
            className="mt-2 w-full text-sm text-purple-300 hover:text-purple-200"
          >
            {isResetting ? "Sending reset email..." : "Forgot your password?"}
          </button>
        </CardContent>
      </Card>
    </div>
  );
};

export default SignInPage;
